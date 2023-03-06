import pymongo
import asyncio

async def get():
    while True:
        conn_string = "mongodb://apiuser:apipass@localhost:27017/criminals_db"
        conn = pymongo.MongoClient(conn_string)
        db = conn["criminals_db"]
        print(list(db["criminals"].find({"entity_id":5})))
asyncio.run(get())