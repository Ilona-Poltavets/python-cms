import os
import re

from sqlalchemy import String, Integer, SmallInteger, BigInteger, Float, Numeric, Boolean, Text, Unicode, UnicodeText, Date, Time, DateTime, Interval, LargeBinary, JSON, Enum

SQLALCHEMY_TYPE_MAP = {
    "string": String,
    "integer": Integer,
    "smallint": SmallInteger,
    "bigint": BigInteger,
    "float": Float,
    "numeric": Numeric,
    "boolean": Boolean,
    "text": Text,
    "unicode": Unicode,
    "unicodetext": UnicodeText,
    "date": Date,
    "time": Time,
    "datetime": DateTime,
    "interval": Interval,
    "binary": LargeBinary,
    "json": JSON,
    "enum": Enum,
}

PYDANTIC_TYPE_MAP = {
    "string": "str",
    "integer": "int",
    "smallint": "int",
    "bigint": "int",
    "float": "float",
    "numeric": "float",
    "boolean": "bool",
    "text": "str",
    "unicode": "str",
    "unicodetext": "str",
    "date": "date",
    "time": "time",
    "datetime": "datetime",
    "interval": "timedelta",
    "binary": "bytes",
    "json": "dict",
    "enum": "str",
}


def string_to_slug(s):
    s = s.lower()
    s = s.replace(' ', '_')
    s = re.sub(r'[^a-z0-9_]', '', s)
    return s


def generate_route_file(slug):
    model_class = slug.capitalize()
    lines = f'''
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from entities.{slug}.{slug}_model import {model_class}Table, {model_class}Schema
from services.db_service import get_db
        
router = APIRouter(prefix="/{slug}", tags=["{slug}"])
        
@router.post("/create")
def create(item: {model_class}Schema, db: Session = Depends(get_db)):
    db_item = {model_class}Table(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
        
@router.get("/read/{{item_id}}")
def read(item_id: int, db: Session = Depends(get_db)):
    item = db.query({model_class}Table).get(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Not found")
    return item
        
@router.put("/update/{{item_id}}")
def update(item_id: int, updated: {model_class}Schema, db: Session = Depends(get_db)):
    item = db.query({model_class}Table).get(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Not found")
    for key, value in updated.dict().items():
        setattr(item, key, value)
    db.commit()
    db.refresh(item)
    return item
        
@router.delete("/delete/{{item_id}}")
def delete(item_id: int, db: Session = Depends(get_db)):
    item = db.query({model_class}Table).get(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Not found")
    db.delete(item)
    db.commit()
    return {{ "detail": "Deleted" }}
        
@router.get("/list")
def list_items(db: Session = Depends(get_db)):
    return db.query({model_class}Table).all()
        '''
    os.makedirs(f"entities/{slug}", exist_ok=True)
    file_path = f"entities/{slug}/{slug}_routes.py"
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(lines.strip())
    print(f"✅ Route file generated: {file_path}")


def generate_model_file(slug, fields):
    model_class = slug.capitalize()
    sqlalchemy_imports = sorted(set(t.__name__ for t in SQLALCHEMY_TYPE_MAP.values()))

    lines = [
        f"from sqlalchemy import Column, {', '.join(sqlalchemy_imports)}",
        "from sqlalchemy.ext.declarative import declarative_base",
        "from pydantic import BaseModel",
        "from datetime import datetime",
        "",
        "Base = declarative_base()",
        "",
        f"class {model_class}Table(Base):",
        f"    __tablename__ = '{slug}'",
        "    id = Column(Integer, primary_key=True)",
    ]

    for field in fields:
        name = field["fieldName"]
        type_ = SQLALCHEMY_TYPE_MAP[field["fieldType"].lower()].__name__
        lines.append(f"    {name} = Column({type_})")

    lines += ["", f"class {model_class}Schema(BaseModel):"]

    for field in fields:
        name = field["fieldName"]
        type_ = PYDANTIC_TYPE_MAP.get(field["fieldType"].lower(), "Any")
        lines.append(f"    {name}: {type_}")

    lines.append("")
    file_path = f"entities/{slug}/{slug}_model.py"
    os.makedirs(f"entities/{slug}", exist_ok=True)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    with open(f"entities/{slug}/__init__.py", "w", encoding="utf-8") as f:
        pass

    print(f"✅ Model file generated: {file_path}")
