from fastapi import APIRouter, Depends
from database import DBMongo
from models import Criminal
import os
from fastapi_pagination import Page, Params, paginate


router = APIRouter(prefix="/api")
MONGO_COLLECTION = os.environ.get("MONGO_COLLECTION")

mongo_db = DBMongo()
@router.get("/", response_model=Page[Criminal])
def get_criminals(params: Params = Depends()):
    db = mongo_db.get_db()
    data = list(db[MONGO_COLLECTION].find({}, {"_id":0}))
    return paginate(data, params)
