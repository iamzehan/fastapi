from typing import *
from fastapi import FastAPI, status

app = FastAPI()


@app.post("/items/", status_code=status.HTTP_201_CREATED)
async def create_item(name: str):
    return {"name": name}

@app.get("/info/", response_model=Union[Dict[str, float], Dict[str,str]], status_code=status.HTTP_200_OK)
async def read_items():
    return {"name":"foo", "Age":20, "Salary": 20000.00}