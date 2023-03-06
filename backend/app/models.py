from pydantic import BaseModel


class Criminal(BaseModel):
    forename = str
    name = str
    date_of_birth = str
    entity_id = str
    thumbnail = str
    url = str