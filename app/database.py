import os
from database import Database
from sqlalchemy import create_engine, MetaData

DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql://user:password@db/dbname")
database = Database(DATABASE_URL)
metadata = MetaData()
engine = create_engine(DATABASE_URL)
