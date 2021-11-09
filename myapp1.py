from typing import Optional, List, Dict, Set

from fastapi import Body, FastAPI, Cookie, Header, Query, Path
from pydantic import BaseModel, Field, EmailStr
from pydantic.networks import HttpUrl, url_regex

app = FastAPI()


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None


@app.put("/items/{item_id}")
async def update_item(
    item_id: int,
    item: Item = Body(
        ...,
        example={
            "name": "Foo",
            "description": "A very nice Item",
            "price": 35.4,
            "tax": 3.2,
        },
    ),
):
    results = {"item_id": item_id, "item": item}
    return results

"""Multiple Examples in the schema (Accessible with a dropdown in the UI)"""

@app.put("/items1/{item_id}")
async def update_item(
    *,
    item_id: int,
    item: Item = Body(
        ...,
        examples={
            "normal": {
                "summary": "A normal example",
                "description": "A **normal** item works correctly.",
                "value": {
                    "name": "Foo",
                    "description": "A very nice Item",
                    "price": 35.4,
                    "tax": 3.2,
                },
            },
            "converted": {
                "summary": "An example with converted data",
                "description": "FastAPI can convert price `strings` to actual `numbers` automatically",
                "value": {
                    "name": "Bar",
                    "price": "35.4",
                },
            },
            "invalid": {
                "summary": "Invalid data is rejected with an error",
                "value": {
                    "name": "Baz",
                    "price": "thirty five point four",
                },
            },
        },
    ),
):
    results = {"item_id": item_id, "item": item}
    return results


"""More datatypes"""
from datetime import datetime, time, timedelta
from typing import Optional
from uuid import UUID

@app.put("/datatypes/{item_id}")
async def read_items(
    item_id: UUID,
    start_datetime: Optional[datetime] = Body(None),
    end_datetime: Optional[datetime] = Body(None),
    repeat_at: Optional[time] = Body(None),
    process_after: Optional[timedelta] = Body(None),
):
    start_process = start_datetime + process_after
    duration = end_datetime - start_process
    return {
        "item_id": item_id,
        "start_datetime": start_datetime,
        "end_datetime": end_datetime,
        "repeat_at": repeat_at,
        "process_after": process_after,
        "start_process": start_process,
        "duration": duration,
    }

@app.put("/manipulate/{item_id}")
async def read_items(
    item_id: UUID,
    start_datetime: Optional[datetime] = Body(None),
    end_datetime: Optional[datetime] = Body(None),
    repeat_at: Optional[time] = Body(None),
    process_after: Optional[timedelta] = Body(None),
):
    start_process = start_datetime + process_after
    duration = end_datetime - start_process
    return {
        "item_id": item_id,
        "start_datetime": start_datetime,
        "end_datetime": end_datetime,
        "repeat_at": repeat_at,
        "process_after": process_after,
        "start_process": start_process,
        "duration": duration,
    }

"""Cookie Parameters"""

@app.get("/cookie/")
async def read_items(ads_id: Optional[str] = Cookie(None)):
    return {"ads_id": ads_id}


"""Headers"""
@app.get("/header/")
async def read_items(user_agent: Optional[str] = Header(None)):
    return {"User-Agent": user_agent}

@app.get("/strange_header/")
async def read_items(
    strange_header: Optional[str] = Header(None, convert_underscores=False)
):
    return {"strange_header": strange_header}

"""Duplicate Headers"""
@app.get("/duplicate_headers/")
async def read_items(x_token: Optional[List[str]] = Header(None)):
    return {"X-Token values": x_token}

class Image(BaseModel):
    url: HttpUrl=Field(None, example="http://www.example.com")
    name: str

@app.put("/multipleimages/")
async def read_item(images: Optional[List[Image]]=Body(...,embed=True)):
    return {"images": images}

"""response model"""
@app.post("/createimage/", response_model=List[Image])
async def create_item(images: List[Image]=Body(...,embed=True)):
    return images



"""Response Model encoding parameters"""
class Encode(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: float = 10.5
    tags: List[str] = []


items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
    "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tags": []},
}


@app.get("/encoding/{item_id}", response_model=Encode, response_model_exclude_unset=True) # You can also use response_model_include and response_model_exclude
async def read_item(item_id: str):
    item_id=item_id.lower()
    return items[item_id]


"""Some password shit going on here"""
class UserIn(BaseModel):
    username: str
    password: str
    email: EmailStr=Field(None, example="user@example.com")
    full_name: Optional[str] = None


class UserOut(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None

class UserInDB(BaseModel):
    username: str
    hashed_password: str
    email: EmailStr
    full_name: Optional[str] = None

# Don't do this in production!
@app.post("/user/", response_model=UserOut)
async def create_user(user: UserIn):
    return user

"""Hashed password, we created an extra model UserInDB"""
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