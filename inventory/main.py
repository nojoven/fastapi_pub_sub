from redis_om import get_redis_connection, HashModel
from fastapi import FastAPI
from setup import REDIS_DB

app = FastAPI()

redis = get_redis_connection(
   host="redis-15098.c299.asia-northeast1-1.gce.cloud.redislabs.com",
   port=15098,
   password=REDIS_DB,
   decode_responses=True
)

class Product(HashModel):
   name: str
   price: float
   available_quantity: int

   class Meta:
      database = redis 



@app.get("/products")
def all():
   return Product.all_pks()