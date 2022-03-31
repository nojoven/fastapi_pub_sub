import requests
import time

from redis_om import get_redis_connection, HashModel

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.background import BackgroundTasks

from starlette.requests import Request

from setup import REDIS_DB, INVENTORY_BASE_URL

app = FastAPI()

app.add_middleware(
   CORSMiddleware,
   allow_origins=["http://localhost:3000"],
   allow_methods=["*"],
   allow_headers=["*"]
)

# In real world it would be a different database
redis = get_redis_connection(
   host="redis-15098.c299.asia-northeast1-1.gce.cloud.redislabs.com",
   port=15098,
   password=REDIS_DB,
   decode_responses=True
)

class Order(HashModel):
    product_id: str 
    price: float
    fee: float
    total: float
    quantity: int
    status: str # pending, completed, refounded
    
    class Meta:
        database = redis


@app.get('/orders/{pk}')
def get(pk: str):
    return Order.get(pk)



@app.post("/orders")
async def create(request: Request, background_task: BackgroundTasks): # id, quantity
    body = await request.json()

    req = requests.get(f"{INVENTORY_BASE_URL}/{body['id']}")
    
    product =  req.json()

    order = Order(
            product_id=body['id'],
            price=product['price'],
            fee=0.2 * product['price'],
            total= 1.2 * product['price'],
            quantity= body['quantity'],
            status='pending'
    )
    order.save()

    background_task.add_task(order_completed, order)

    return order

def order_completed(order: Order):
    time.sleep(5)
    order.status = 'completed'
    order.save()
