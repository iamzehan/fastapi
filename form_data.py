from fastapi import FastAPI, Form, status
from pydantic import BaseModel, EmailStr
app = FastAPI()


@app.post("/login/")
async def login(username: str = Form(...), password: str = Form(...), status_code=status.HTTP_202_ACCEPTED):
    return {"username": username}

@app.post("/register/")
async def register(username: str = Form(...),first_name:str=Form(...), last_name:str=Form(...),email:EmailStr=Form(..., example="mymail@example.com"), password: str = Form(...), confirm_password: str = Form(...), status_code=status.HTTP_201_CREATED):
    return {"name": first_name+" "+last_name, "message": f"Welcome {first_name.title()}!"}