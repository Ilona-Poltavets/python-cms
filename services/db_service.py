import os

import sqlalchemy
from fastapi import HTTPException
from sqlalchemy import Column, Integer, String, Text, Table, Boolean, Float, DateTime, inspect, MetaData
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.exc import ProgrammingError
from sqlalchemy import text

from dotenv import load_dotenv

load_dotenv()
ENVIRONMENT_MODE = os.getenv('ENVIRONMENT_MODE')


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
                metadata = MetaData()
                entities_table = Table(
                    'entities',
                    metadata,
                    Column('id', Integer, primary_key=True, autoincrement=True),
                    Column('name', String, nullable=False),
                    Column('slug', String, nullable=False),
                    Column('table_name', String, nullable=False),
                )
                metadata.create_all(engine)
                print("✅ Table 'entities' created.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"❌ DB connection failed: {str(e)}")
