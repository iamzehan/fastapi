from typing import List
from fastapi import FastAPI, File, UploadFile, status, Form
from fastapi.responses import HTMLResponse

app = FastAPI()


@app.post("/files/")
async def create_file(files: List[bytes] = File(...)): #gets stored in the memory
    return {"file_size": [len(file) for file in files]}


@app.post("/uploadfiles/", status_code=status.HTTP_202_ACCEPTED)
async def create_upload_files(username: str=Form(...),files: List[UploadFile] = File(...)):
    ls=[]
    for file in files:
        ls.append({"filenames": file.filename, "type": file.content_type})
    return {"username": username, "files": ls}

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
    <h1>Upload Images</h1>
        <div class="container">
            <form action="/files/" enctype="multipart/form-data" method="post">
                <input name="files" type="file" multiple>
                <input type="submit">
            </form>
        </div>
        <br>
        <div class="container">
            <form action="/uploadfiles/" enctype="multipart/form-data" method="post">
                <label for="files">Upload:</label>
                <input name="files" type="file" multiple>
                <label for="username">Username:</label>
                <input name="username" type="text" placeholder="Username">
                <input type="submit">
            </form>
        </div>
    </body>
    """
    return HTMLResponse(content=content)

