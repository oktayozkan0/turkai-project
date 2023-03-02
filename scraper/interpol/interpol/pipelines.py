import pika
from scrapy.utils.serialize import ScrapyJSONEncoder
import os


class RabbitMQPipeline:
    def __init__(self) -> None:
        self.host = os.environ.get("RABBITMQ_HOST")
        self.amqp_port = int(os.environ.get("RABBITMQ_AMQP_PORT"))
        self.rabbit_q = os.environ.get("RABBITMQ_QUEUE")
        self.encoder = ScrapyJSONEncoder()

    def open_spider(self, spider):
        credentials = pika.PlainCredentials('guest', 'gueset')
        params = pika.ConnectionParameters(self.host,
                                        self.amqp_port,
                                        "/",
                                        credentials)
        conn = pika.BlockingConnection(params)
        params.heartbeat = 900
        conn = pika.BlockingConnection(params)
        self._channel = conn.channel()
        self._channel.queue_declare(queue=self.rabbit_q, durable=True)
    
    def close_spider(self, spider):
        self._channel.close()
    
    def process_item(self, item, spider):
        data = self.encoder.encode(item)
        self._channel.basic_publish(body=data, exchange="", routing_key=self.rabbit_q)
        return item
