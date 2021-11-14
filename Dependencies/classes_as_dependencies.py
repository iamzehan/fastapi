from typing import Optional

from fastapi import Depends, FastAPI

app = FastAPI()


fake_items_db = [{"name": "Nivea","class": "cream", "description": "It is a sunscreen","brand": "Berisdorf AG", "price": 152.0},
                {"name": "Vaseline Lotion", "class": "lotion", "description": "It is a body lotion", "brand": "Uniliever", "price": 195.0}, 
                {"name": "Parachute Lotion", "class": "lotion", "description": "It is a body lotion", "brand": "Merico", "price": 170.0}, 
                {"name": "fair & lovely", "class": "cream", "description": "It is a sunscreen", "brand": "Uniliever", "price": 50.0},
                {"name": "Team Force", "class": "Body Spray", "description": "Perfume Body Spray", "brand": "Adidas", "price": 350.0}]



class CommonQueryParams:

    def __init__(self, q: Optional[str] = None, skip: int = 0, limit: int = 100):

        self.q = q

        self.skip = skip

        self.limit = limit



@app.get("/items/")
async def read_items(commons: CommonQueryParams = Depends()):
    response = {}
    ls=[]
    count=0
    
    for item in fake_items_db:
        for k in item:
            if type(item[k])==int:
                response.update({"q": commons.q})
                items=fake_items_db[count]
                if items not in ls:
                    ls.append(items)
            elif type(item[k])==str:
                if commons.q.casefold() in item[k].casefold():
                    response.update({"q": commons.q})
                    items=fake_items_db[count]
                    if items not in ls:
                        ls.append(items)
        count+=1
    if ls:
        if len(ls)>1:
            response.update({"searched items":ls})
        else:
            response.update({"searched items":items})
    else:
        response.update({"q": f"'{commons.q}' not found, below are the list of available items"})
        items = fake_items_db[commons.skip : commons.skip + commons.limit]
        response.update({"items": items})
    return response
