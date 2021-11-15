# fastapi
Learning Curve

## Clone this repository

            git clone https://github.com/iamzehan/fastapi.git
            
## Create Virtual Environment

            virtualenv <env_name>
     
## Activate Envrionment

            <env_folder>\Script\activate

## Install dependencies
(Assuming you have pip and python already installed)

            pip install -r requirement.txt
## Run Project
            uvicorn: python_file:app 
### Or
            uvicorn: python_file:app --relaoad
  
  <code>
  app= FastAPI()
  
  _pythonfile: file you're working with_
</code>
## Open in Browser
            http://127.0.0.1:8000/

## Open Docs
            http://127.0.0.1:8000/docs
            
## Generate random SECRET KEY
<code>** git bash cli required </code>
           
           openssl rand -hex 32
