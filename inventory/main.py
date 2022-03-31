from redis_om import get_redis_connection, HashModel
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from setup import REDIS_DB

app = FastAPI()

app.add_middleware(
   CORSMiddleware,
   allow_origins=["http://localhost:3000"],
   allow_methods=["*"],
   allow_headers=["*"],
)

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
   return [format(pk) for pk in Product.all_pks()]


def format(pk: str):
   product = Product.get(pk)

   return {
      'id': product.pk,
      'name': product.name, 
      'price': product.price,
      'available_quantity': product.available_quantity,
   }

@app.post("/products")
def create(product: Product):
   return product.save()

@app.get("/products/{pk}")
def get(pk: str):
   return Product.get(pk)


@app.delete("/products/{pk}")
def delete(pk: str):
   return Product.delete(pk)
