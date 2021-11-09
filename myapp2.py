from typing import Optional,Union,List, Dict

from fastapi import FastAPI
from pydantic import BaseModel, EmailStr

app = FastAPI()


class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None


class UserIn(UserBase):
    password: str


class UserOut(UserBase):
    pass


class UserInDB(UserBase):
    hashed_password: str


def fake_password_hasher(raw_password: str):
    return "supersecret" + raw_password


def fake_save_user(user_in: UserIn):
    hashed_password = fake_password_hasher(user_in.password)
    user_in_db = UserInDB(**user_in.dict(), hashed_password=hashed_password)
    print("User saved! ..not really")
    return user_in_db


@app.post("/user/", response_model=UserOut)
async def create_user(user_in: UserIn):
    user_saved = fake_save_user(user_in)
    return user_saved

class BaseItem(BaseModel):
    description: str
    type: str


class CarItem(BaseItem):
    type = "car"


class PlaneItem(BaseItem):
    type = "plane"
    size: int


items = {
    "item1": {"description": "All my friends drive a low rider", "type": "car"},
    "item2": {
        "description": "Music is my aeroplane, it's my aeroplane",
        "type": "plane",
        "size": 5,
    },
}


@app.get("/items/{item_id}", response_model=Union[PlaneItem, CarItem]) #it could be either of these models, but depending on the item_id
async def read_item(item_id: str):
    return items[item_id]

"""List of Models"""
class Item(BaseModel):
    name: str
    description: str


items = [
    {"name": "Ironman", "description": "There comes my hero"},
    {"name": "Captain America", "description": "Here comes the first Avenger"},
]


@app.get("/items/", response_model=List[Item])
async def read_items():
    return items

"""Response with Arbitrary Dictionary"""

@app.get("/info/", response_model=Union[Dict[str, float], Dict[str,str]])
async def read_items():
    return {"name":"foo", "Age":20, "Salary": 20000.00}