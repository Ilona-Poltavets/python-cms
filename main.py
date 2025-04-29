import os
from pathlib import Path

from fastapi import FastAPI,Request
from sqlalchemy import create_engine
from starlette.responses import HTMLResponse
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from services.db_service import check_connection

app=FastAPI()
POSTGRES_URL = os.getenv("POSTGRES_URL")
engine = create_engine(POSTGRES_URL)
templates = Jinja2Templates(directory="views")
app.mount("/src", StaticFiles(directory="src"), name="src")

@app.on_event("startup")
async def startup_event():
    try:
        check_connection(engine)
    except Exception as e:
        print(f"⚠️ Warning: DB startup check failed: {e}")

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/entities", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("entities.html", {"request": request})