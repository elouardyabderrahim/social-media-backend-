# social-media-backend-
This a social media clone where user can post and other users can vote on posts I use fastAPI to create the backend .

## Prerequisites

- Python 3.6 or higher installed on your system
- Git installed on your system

## Setup Instructions

### 1. Clone the Repository

First, clone the repository to your local machine:

``` bash
git clone https://github.com/elouardyabderrahim/social-media-backend-.git
cd social-media-backend-
```

###  2. Create a Virtual Environment
Create a virtual environment to manage dependencies:

python -m venv venv

### 3. Activate the Virtual Environment
Activate the virtual environment:

On Windows:

``` bash
.\venv\Scripts\activate

```
On macOS/Linux:

``` bash
source venv/bin/activate
``` 

### 4. Install Dependencies
Install the required dependencies using requirements.txt:

``` bash

pip install -r requirements.txt
``` 

### 5. Run the Application
Start the FastAPI application using Uvicorn:

```  bash
fastapi dev main.py 
```

 Serving at: http://127.0.0.1:8000                
 │                                                   
 API docs: http://127.0.0.1:8000/docs   

Project Structure

``` css
social-media-backend-/
├── venv/
├── main.py
├── requirements.txt
└── README.md
``` 
main.py
```  python
from typing import Union
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
``` 

requirements.txt
``` makefile
fastapi[all]
``` 
### used laibraries :

fastapi
Pydantic: Schema Validation. 

### Notes
Make sure to always activate the virtual environment before running the application.
If you make changes to the dependencies, remember to update requirements.txt by running `pip freeze > requirements.txt`.