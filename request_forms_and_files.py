from typing import Optional
from fastapi import FastAPI, File, Form, UploadFile, status
from fastapi.datastructures import Default

app = FastAPI()


@app.post("/files/", status_code=status.HTTP_202_ACCEPTED)
async def create_file(
    file: bytes = File(...), fileb: UploadFile = File(...), token: Optional[str] = Form(None)
):
    return {
        "file_size": len(file),
        "token": token,
        "fileb_content_type": fileb.content_type,
    }

