from fastapi import FastAPI
#uvicorn main:app --reload <------------ use this command to run the server ------------<<<<<
from typing import Optional
from enum import Enum
from pydantic import BaseModel
class AIModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

myapi = FastAPI()


@myapi.get("/")
async def root():
    return {"message": "Hello World"}
def read_items(item_id):
    return {"id": item_id}

@myapi.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}

@myapi.get("/hi")
def say_hi_to_mark():
    return { "message": "Oh, Hi Mark!"}
@myapi.get("/users/me")
async def read_user_me():
    return {"user_id": "The Current user"}
@myapi.get("/users/{user_id}")
async def read_user(user_id: int):
    return {"user_id": user_id}

@myapi.get("/models/{model_name}")
async def get_model(model_name: AIModelName):
    if model_name == AIModelName.alexnet:
        id=1
        return {"id": id, "model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        id=2
        return {"id": id,"model_name": model_name, "message": "LeCNN all the images"}

    return {"id":3, "model_name": model_name, "message": "Have some residuals"}


@myapi.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}

fake_items_db = [{"item_id":"1", "item_name": "Foo"}, {"item_id":"2","item_name": "Bar"}, {"item_id":"3","item_name": "Baz"}]


@myapi.get("/items/")
async def read_items(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]


@myapi.get("/search/{query}")
async def search_item(query: str):
    query=query.title()
    count=0
    ls=[]
    for dicts in fake_items_db:
        if query==dicts["item_id"]:
            ls.append(fake_items_db[count])
        elif query in dicts["item_name"].title():
            ls.append(fake_items_db[count])
        count+=1
    if not ls:
        return None
    else:
        return ls




class Item(BaseModel):
    item_name: str
    description: Optional[str] = None
    price: Optional[float] = None
    tax: Optional[float] = None

@myapi.post("/items/")
async def create_item(item: Item):
    item.item_name=item.item_name.title()
    return item
@myapi.post("/create-items/")
async def create_item(item: Item):
    item.item_name=item.item_name.title()
    item_dict = item.dict()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict

@myapi.put("/items/{item_id}")
async def create_item(item_id: int, item: Item, q: Optional[str]=None):
    result = {"item_id": item_id, **item.dict()}
    if q:
        result.update({"q": q})
    return result