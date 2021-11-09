from os import name
from typing import Counter, Optional, List
from fastapi import FastAPI,Query
from pydantic import BaseModel

class Info(BaseModel):
    id: str
    name: str
    age: int
app=FastAPI()

@app.post("/user/{id}")
async def user_info(id: str, info: Info):
    info.id=id
    return info.dict()

# @app.get("/items/")
# async def read_items(q: Optional[str] = None):
#     results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
#     if q:
#         results.update({"q": q})
#     return results
@app.get("/items/")
async def read_items(q: Optional[str] = Query(None, max_length=50)):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    # if q:
    #     results.update({"q": q})
    # return results
    ls=[]
    count=0
    if q:
        for item in results["items"]:
            if (item["item_id"]==q):
                ls.append(results["items"][count])
            count+=1
        return ls
    else:
        return results

#>>>>>>>>----------Regular Expressions--------<<<<<<<<
@app.get("/item/")
async def read_items(
    q: Optional[str] = Query(None, min_length=3, max_length=50, regex="^fixedquery$")
):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results
@app.get("/itemslist/")
async def read_items(q: Optional[List[str]] = Query(None)):
    query_items = {"q": q}
    return query_items
@app.get("/addtitle/")
async def read_items(q: Optional[str] = Query(None,
                                            title="Add title, description, Alias names for the api",
                                            description="Query string for the items to search in the database that have a good match",
                                            alias="item-query", 
                                            min_length=3
                                            )
                    ):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


"""Now let's say you don't like this parameter anymore.

You have to leave it there a while because there are clients using it, but you want the docs to clearly show it as deprecated.

Then pass the parameter deprecated=True to Query
"""

@app.get("/deprecated/")
async def deprecated_parameter(
    q: Optional[str] = Query(
        None,
        alias="item-query",
        title="Query string",
        description="Please use the parameter 'add title' instead",
        min_length=3,
        max_length=50,
        regex="^fixedquery$",
        deprecated=True,
    )
):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


"""Path Parameters and Numeric Validations, 
You can declare all the metadata like descriptions and title as you have done it in query
In python the default parameters have to come last, standard parameter comes first, then *args, then defaults, then **kwargs.
But in FastAPI ---It doesn't matter. It will detect the parameters by their names, types and default declarations (Query, Path, etc), 
it doesn't care about the order."""

from fastapi import Path, Body
@app.get("/pathparameters/{item_id}")
async def read_items(
    item_id: int = Path(..., title="The ID of the item to get"),
    q: Optional[str] = Query(None, alias="item-query", description="Here we are using both path and query"),
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results

"""Order the parameters as you need"""
@app.get("/orderparameters/{item_id}")
async def read_items(
    *, item_id: int = Path(..., title="The ID of the item to get"), q: str
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results

"""Number validations: greater than or equal
ge: greater than or equal
le: less than or equal

---for floats

gt: greater than (you can use float number)
lt: less than (you can use float numbers as well)

'*' is passed so that the latter arguments are taken as 'kwargs' or keyword arguments"""

db = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
l=len(db["items"])
@app.get("/numbervalidations/{item_id}")
async def read_items(
    *, item_id: int = Path(..., title="The ID of the item to get", ge=1, le=l), q: str
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results

"""Body Parameters"""
@app.put("/bodyparam/{item_id}")
async def update_item(
    *,
    primary_key: int = Path(..., title="The ID of the item to get", ge=0, le=1000),
    q: Optional[str] = None,
    item: Optional[Info] = None,
):
    results = {"Primary Key": primary_key}
    if q:
        results.update({"q": q})
    if item:
        results.update({"student": item})
    return results

"""Multiple body Parameters"""
class Student(BaseModel):
    id: str
    first_name: str
    second_name: str
    age: int
class User(Student,BaseModel):
    username: str
    full_name: Optional[str] = None


@app.put("/multibodyparam/{item_id}")
async def update_item(*,primary_key:int=1, student: Student=Body(..., embed=True), user: User=Body(..., embed=True), importance: int = Body(...)):
    user.username=student.first_name.lower()
    user.first_name=student.first_name.title()
    user.second_name=student.second_name.title()
    user.age=student.age
    user.full_name=student.first_name+" "+student.second_name
    user.id=student.id
    results = {"primary_key": primary_key, "student": student, "user": user}
    return results


"""Fields, you can see them in the Schemas options"""
from typing import Set, Dict
from pydantic import Field,HttpUrl
class Teacher(BaseModel):
    name: str
    description: Optional[str] = Field(
        None, title="The description of the item", max_length=300
    )
    Salary: float = Field(..., gt=0, description="The price must be greater than zero")
    department: Set[str] =set()



@app.put("/teachers/{item_id}")
async def update_item(item_id: int, teacher: Teacher = Body(..., embed=True)):
    results = {"item_id": item_id, "item": teacher}
    return results

class Image(BaseModel):
    url: HttpUrl=Field(None,
        example="http://www.example.com", title="Must be a valid url")
    name: str


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None
    tags: Set[str] = []
    image: Optional[Image] = None #we are using url, name attributes from 'Image' model here
    thumbnails: Optional[List[Image]]

class Offer(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    discount: float = 0.1
    items: List[Item]

@app.put("/nestedbody/{item_id}")
async def update_item(item_id: int, item: Item):
    results = {"item_id": item_id, "item": item}
    return results

@app.put("/offers/{item_id}")

async def update_item(item_id: int, d: Optional[float]=Query(0.1,alias="item-discount"), offer: Offer=Body(..., embed=True)):
    offer.price= offer.items.price*d 
    results = {"item_id": item_id, "offer": offer}
    return results["offer"]
@app.post("/images/multiple/")
async def create_multiple_images(*,images: List[Image]):
    for image in images:
        image.url
        return images

@app.post("/index-weights/")
async def create_index_weights(weights: Dict[int, float]):
    return weights
"""
in the example above it will take keys and values as, because pydantic models take 'str' as keys
{
  "1": 1.0,
  "2": 1.9,
  "3": 1.3
}"""

"""------Schema Extra------
You can setup examples in here"""
class Reserve(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None

    class Config:
        schema_extra = {
            "example": {
                "name": "Foo",
                "description": "A very nice Item",
                "price": 35.4,
                "tax": 3.2,
            }
        }


@app.put("/reserves/{item_id}")
async def update_item(item_id: int, item: Reserve):
    results = {"item_id": item_id, "item": item}
    return results


"""Field Additional arguments"""
class FieldAdditional(BaseModel):
    name: str = Field(..., example="Foo")
    description: Optional[str] = Field(None, example="A very nice Item")
    price: float = Field(..., example=35.4)
    tax: Optional[float] = Field(None, example=3.2)


@app.put("/fieldextra/{item_id}")
async def update_item(item_id: int, item: FieldAdditional):
    results = {"item_id": item_id, "item": item}
    return results

