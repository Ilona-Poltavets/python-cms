from sqlalchemy import Table, Column, Integer, String, MetaData
from sqlalchemy.ext.declarative import declarative_base

metadata = MetaData()
Base = declarative_base()

entities = Table(
    'entities',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String),
    Column('slug', String),
    Column('table_name', String),
)

class EntityTable(Base):
    __tablename__='entities'
    id= Column(Integer, primary_key=True)
    name= Column(String)
    slug=Column(String)
    table_name=Column(String)