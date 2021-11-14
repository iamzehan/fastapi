from fastapi import Depends, FastAPI, Header, HTTPException

app = FastAPI()

users=[{"username":"abcd", "credentials":{"key": "fake-super-secret-token", "token": "fake-super-secret-token"}}]
async def verify_token(x_token: str = Header(...)):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")


async def verify_key(x_key: str = Header(...)):
    if x_key != "fake-super-secret-key":
        raise HTTPException(status_code=400, detail="X-Key header invalid")
    return x_key


@app.get("/home/", dependencies=[Depends(verify_token), Depends(verify_key)])
async def read_items():
    return [{"item": "Foo"}, {"item": "Bar"}]



"""In this case we don't need to return the value of token and verification key
So, our path decorator @app is receiving a parameter - 'dependencies' which is a list of dependencies"""