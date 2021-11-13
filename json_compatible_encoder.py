"""There are some cases where you might need to convert a data type (like a Pydantic model)

 to something compatible with JSON (like a dict, list, etc).

For example, if you need to store it in a database.

For that, FastAPI provides a jsonable_encoder() function."""

from datetime import datetime
from typing import Optional

from fastapi import FastAPI

from fastapi.encoders import jsonable_encoder

from pydantic import BaseModel


fake_db = {}


class Item(BaseModel):
    title: str
    timestamp: datetime
    description: Optional[str] = None


app = FastAPI()


@app.put("/items/{id}")
def update_item(id: str, item: Item):
    item.timestamp = item.timestamp.strftime("%d/%m/%Y, %I:%M:%S")
    json_compatible_item_data = jsonable_encoder(item)

    fake_db[id] = json_compatible_item_data

    return fake_db[id]
