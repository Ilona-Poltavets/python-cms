import os
from pathlib import Path

from fastapi import FastAPI, Request, Body
from sqlalchemy import create_engine
from starlette.responses import HTMLResponse
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
from pydantic import BaseModel
from typing import Annotated, List

from services.db_service import check_connection, add_new_entity, create_entity_table
from utils.string_utils import string_to_slug, generate_model_file, generate_route_file

app = FastAPI()
POSTGRES_URL = os.getenv("POSTGRES_URL")
engine = create_engine(POSTGRES_URL)
templates = Jinja2Templates(directory="views")
app.mount("/src", StaticFiles(directory="src"), name="src")


class Entity(BaseModel):
    entityName: str
    fields: List[dict]


@app.on_event("startup")
async def startup_event():
    try:
        check_connection(engine)
    except Exception as e:
        print(f"⚠️ Warning: DB startup check failed: {e}")


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/entities", response_class=HTMLResponse)
def list_entities(request: Request):
    return templates.TemplateResponse("entities.html", {"request": request})


@app.get("/entities/create", response_class=HTMLResponse)
def create_entity_page(request: Request):
    return templates.TemplateResponse("entities.create.html", {"request": request})


@app.post("/create-entity")
def create_entity(entity: Annotated[Entity, Body(embed=True)]):
    slug = string_to_slug(entity.entityName)
    add_new_entity(engine, entity.entityName, slug)
    create_entity_table(engine, slug, entity.fields)
    # os.makedirs('entities', exist_ok=True)
    generate_model_file(slug, entity.fields)
    generate_route_file(slug)
    return {'info': 'it is working'}
