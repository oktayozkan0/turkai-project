from fastapi import APIRouter
from database import DBMongo
import os


router = APIRouter(prefix="/api")
MONGO_COLLECTION = os.environ.get("MONGO_COLLECTION")

@router.get("/")
def get_criminals():
    db = DBMongo.get_db()
    data = db[MONGO_COLLECTION].find({})
    return list(data)
