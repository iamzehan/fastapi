from typing import Optional
from fastapi import FastAPI, HTTPException, status, Request
from fastapi.param_functions import Query
from fastapi.responses import HTMLResponse, JSONResponse

app = FastAPI()

items = {"foo": "The Foo Wrestlers", "bar": "The bartenders"}


@app.get("/items/", status_code=status.HTTP_200_OK)
async def read_item(item_id: Optional[str] = Query(..., max_length=50)):
    item_id=item_id.casefold()
    if item_id not in items:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return {"item": items[item_id]}

@app.get("/")
async def main():
    content = """
    <head>
        <style> 
            input[type=submit] {
            background-color: #4CAF50;
            color: white;
            padding: 12px 20px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            float: middle;
            }

            input[type=text] {
            width: 20%;
            padding: 12px 20px;
            margin: 8px 0;
            box-sizing: border-box;
            border-radius: 5px;
            border: 2px solid black;
            background-color: #f2f2f2;
            }
            .container {
            border-radius: 5px;
            background-color: #f2f2f2;
            padding: 100px;
            width: 40%;
            display: block;
            margin-left: auto;
            margin-right: auto;
            }
            h1{
                text-align: center;
            }
        </style>
    </head>
    <body>
    <h1>Search Items</h1>
        <div class="container">
            <form action="/items/" enctype="multipart/form-data" method="get">
                <input name="item_id" type="text">
                <input type="submit" value="Search">
            </form>
        </div>
        <br>
    </body>
    """
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