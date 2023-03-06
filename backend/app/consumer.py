import pika
import os
from database import db
import json
import time


def consume_data():
    host = "rabbitmq"
    rabbit_user = os.environ.get("RABBITMQ_DEFAULT_USER")
    rabbit_pass = os.environ.get("RABBITMQ_DEFAULT_PASS")
    amqp_port = os.environ.get("RABBITMQ_AMQP_PORT")
    rabbit_q = os.environ.get("RABBITMQ_QUEUE")
    
    
    credentials = pika.PlainCredentials(rabbit_user,
                                        rabbit_pass)
    
    params = pika.ConnectionParameters(host,
                                    amqp_port,
                                    "/",
                                    credentials)

    conn = pika.BlockingConnection(params)
    channel = conn.channel()
    channel.queue_declare(queue=rabbit_q, durable=True)
    method_frame, header_frame, body = channel.basic_get(rabbit_q, auto_ack = True)
    return json.loads(body)

async def to_mongo():
    while True:
        data = consume_data()
        if data is not None:
            db.insert_one(data)
        else:
            time.sleep(30)
