from werkzeug import Request
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from redis_om import get_redis_connection, HashModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:3000'],
    allow_methods=['*'],
    allow_headers=['*']
)

redis = get_redis_connection(
    host="redis-17261.c285.us-west-2-2.ec2.cloud.redislabs.com:17261",
    port=17261,
    password="EGXiGp8zaTA2IeBtB85zHAkSpaRh567Z",
    decode_responses=True
)

class Delivery(HashModel):
    budget: int = 0
    notes: str = ""

    class Meta:
        database = redis

class Event(HashModel):
    delivery_id: str = None
    type: str 
    data: str

    class Meta:
        database = redis

@app.post('/deliveries/create')
async def create(request: Request):
    body = await request.json()
    delivery = Delivery(budget=body['data']['budget'], notes=body['data']['notes']).save()
    return delivery