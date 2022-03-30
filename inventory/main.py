from redis_om import get_redis_connection
from fastapi import FastAPI
from setup import REDIS_DB

app = FastAPI()

redis = get_redis_connection(
   host=REDIS_DB,
   port=15098,
   password="",
   decode_responses=True
)

@app.get("/")
async def root():
    return {"message": "Hello World"}