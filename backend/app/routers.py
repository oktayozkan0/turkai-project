from fastapi import APIRouter
from models import Criminal
from database import db
import os

api = APIRouter()
MONGO_COLLECTION = os.environ.get("MONGO_COLLECTION")
@api.get("/")
def get_criminals():
    data = db[MONGO_COLLECTION].find({})
    return list(data)

