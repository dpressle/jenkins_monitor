import asyncio
import aio_pika
import os

from fastapi import FastAPI
from dotenv import load_dotenv

from app.api.consumer import on_message

app = FastAPI()

load_dotenv()
# Database url if none is passed the default one is used
MQ_QUEUE = os.getenv(
    "MQ_QUEUE")
MQ_URL = os.getenv(
    "MQ_URL", "amqp://mq/")


@app.on_event("startup")
async def startup():
    loop = asyncio.get_event_loop()
    connection = await aio_pika.connect(MQ_URL, loop=loop)
    channel = await connection.channel()
    queue = await channel.declare_queue(MQ_QUEUE)
    await queue.consume(on_message, no_ack=True)
