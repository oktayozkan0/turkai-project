import pika
from scrapy.utils.serialize import ScrapyJSONEncoder


class RabbitMQPipeline:
    def __init__(self, rabbit_uri, rabbit_q) -> None:
        #self.rabbit_uri = "amqp://guest:guest@localhost:5672/"
        self.rabbit_uri = rabbit_uri
        self.rabbit_q = rabbit_q
        self.encoder = ScrapyJSONEncoder()

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            rabbit_uri=crawler.settings.get('RABBITMQ_URI'),
            rabbit_q=crawler.settings.get('RABBITMQ_Q')
        )

    def open_spider(self, spider):
        params = pika.URLParameters(self.rabbit_uri)
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
