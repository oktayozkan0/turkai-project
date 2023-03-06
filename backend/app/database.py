from pymongo import MongoClient
import os


mongo_user = os.environ.get("MONGO_API_USER")
mongo_pass = os.environ.get("MONGO_API_PASS")
mongo_port = os.environ.get("MONGO_PORT")
mongo_collection = os.environ.get("MONGO_COLLECTION")
conn = MongoClient(f"mongodb://{mongo_user}:{mongo_pass}@mongodb:{mongo_port}/{mongo_collection}")

