from typing import Optional
from fastapi import FastAPI, HTTPException, status, Request
from fastapi.param_functions import Query
from fastapi.responses import HTMLResponse, JSONResponse

app = FastAPI()

items = [{"imagine dragons": "Believer"}, 
        {"imagine dragons": "Warriors"}, 
        {"banners": "Start a Riot"}, 
        {"banners": "Too Soon"}, 
        {"banners": "I wanna be somebody"}, 
        {"fall out boy": "Centuries"},
        {"eminem": "Godzilla"}]

@app.get("/items/", status_code=status.HTTP_200_OK)
async def read_item(item_id: Optional[str] = Query(..., max_length=50)):
        item_id=item_id.casefold()
        ls=[]
        count=0
        for item in items:
            if item_id in item:
                count=0
                for artists in item:
                    if artists==item_id:
                        ls.append(item[item_id])
                    count+=1
            count+=1
        if ls:
            return {"songs": ls }
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Song not found")


@app.get("/")
async def main():
    with open('search.html', 'r') as f:
        search = f.read()
    content = search
    return HTMLResponse(content=content)

@app.get("/items-header/{item_id}")
async def read_item_header(item_id: str):
    if item_id not in items:
        raise HTTPException(
            status_code=404,
            detail="Item not found",
            headers={"X-Error": "There goes my error"},
        )
    return {"item": items[item_id]}

#---------Custom Exception-----------
class UnicornException(Exception):
    def __init__(self, name: str):
        self.name = name


@app.exception_handler(UnicornException)
async def unicorn_exception_handler(request: Request, exc: UnicornException):
    return JSONResponse(
        status_code=418,
        content={"message": f"Oops! {exc.name} did something. There goes a rainbow..."},
    )


@app.get("/unicorns/{name}")
async def read_unicorn(name: str):
    if name == "yolo":
        raise UnicornException(name=name)
    return {"unicorn_name": name}

"""Here, if you request /unicorns/yolo, the path operation will raise a UnicornException."""