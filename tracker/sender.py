import pika
import json
import asyncio
import aio_pika

tracker = {
    "state": 'STARTED',
    "url": 'https://sw-jenkins.com/job/cdsoftwarebuilder/job/create-binaries/16280/',
    "parameters": { "version":"0.1.0", "revision":"2"},
    "status": ""
}

connection = pika.BlockingConnection(
    pika.ConnectionParameters("mq"))
channel = connection.channel()
channel.queue_declare(queue='builds')

channel.basic_publish(exchange='', routing_key='builds',
                      body=json.dumps(tracker))
print(" [x] Sent 'Logs'")
connection.close()
