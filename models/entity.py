from sqlalchemy import Table, Column, Integer, String, MetaData

metadata = MetaData()

entities = Table(
    'entities',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String),
    Column('slug', String),
    Column('table_name', String),
)