import os

import sqlalchemy
from fastapi import HTTPException
from sqlalchemy import Column, Integer, String, Text, Table, Boolean, Float, DateTime, inspect, MetaData, SmallInteger, BigInteger, Numeric, Unicode, UnicodeText, Time, Date, Interval, LargeBinary, \
    JSON, Enum, create_engine
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.exc import ProgrammingError
from sqlalchemy import text

from dotenv import load_dotenv
from sqlalchemy.orm import Session, sessionmaker

from models.entity import entities
from models.entity import metadata

load_dotenv()
ENVIRONMENT_MODE = os.getenv('ENVIRONMENT_MODE')

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


def check_connection(engine):
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            print("✅ DB connection successful:", result.scalar())
            inspector = inspect(engine)
            if 'entities' in inspector.get_table_names():
                print("✅ Table 'entities' exists.")
            else:
                print("⚠️ Table 'entities' does not exist. Creating it...")
                metadata.create_all(engine)
                print("✅ Table 'entities' created.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"❌ DB connection failed: {str(e)}")


def add_new_entity(engine, name, slug):
    with Session(engine) as session:
        stmt = insert(entities).values(name=name, slug=slug, table_name=slug)
        session.execute(stmt)
        session.commit()


def create_entity_table(engine, slug, fields):
    metadata = MetaData()
    inspector = inspect(engine)

    if slug in inspector.get_table_names():
        print(f"⚠️ Table '{slug}' already exists. Skipping creation.")
        return

    columns = [Column('id', Integer, primary_key=True, autoincrement=True)]
    for field in fields:
        field_name = field['fieldName']
        field_type = field['fieldType'].lower()

        sqlalchemy_type = SQLALCHEMY_TYPE_MAP.get(field_type, String)
        columns.append(Column(field_name, sqlalchemy_type))

    Table(slug, metadata, *columns)
    metadata.create_all(engine)


def get_db() -> Session:
    load_dotenv()

    DATABASE_URL = os.getenv("POSTGRES_URL")

    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
