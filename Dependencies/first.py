from typing import Optional

from fastapi import Depends, FastAPI

app = FastAPI()



async def common_parameters(q: Optional[str] = None, skip: int = 0, limit: int = 100):

    return {"q": q, "skip": skip, "limit": limit}


"""Both items and users share the same parameters by the Depends() function, more like inheritence"""

@app.get("/items/")
async def read_items(commons: dict = Depends(common_parameters)):
    return commons


@app.get("/users/")
async def read_users(commons: dict = Depends(common_parameters)):
    return commons
