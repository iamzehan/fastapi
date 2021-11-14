from typing import Optional

from fastapi import Depends, FastAPI

app = FastAPI()



async def common_parameters(q: Optional[str] = None, skip: int = 0, limit: int = 100):

    return {"q": q, "skip": skip, "limit": limit}


"""Both items and users share the same parameters by the Depends() function,
more like inheritence, but only takes a single parameter"""

@app.get("/items/")
async def read_items(commons: dict = Depends(common_parameters)):
    return commons


@app.get("/users/")
async def read_users(commons: dict = Depends(common_parameters)):
    return commons

"""FastAPI compatibility
The simplicity of the dependency injection system makes FastAPI compatible with:

 * all the relational databases
 * NoSQL databases
 * external packages
 * external APIs
 * authentication and authorization systems
 * API usage monitoring systems
 * response data injection systems
etc."""