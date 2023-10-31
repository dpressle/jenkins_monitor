from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

# import asyncio
# import aio_pika

from app.routes import ping, releases, builds
from app.db import engine, metadata, database
from app.api.consumer import on_message

metadata.create_all(engine)

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:5173",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["DELETE", "GET", "POST", "PUT"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    await database.connect()
    # loop = asyncio.get_event_loop()
    # connection = await aio_pika.connect("amqp://mq/", loop=loop)
    # channel = await connection.channel()
    # queue = await channel.declare_queue("builds")
    # await queue.consume(on_message, no_ack=True)


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


app.include_router(ping.router)
app.include_router(builds.router, prefix="/builds", tags=["builds"])
app.include_router(releases.router, prefix="/releases", tags=["releases"])
