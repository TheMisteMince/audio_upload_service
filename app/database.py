import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import MetaData
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql+asyncpg://user:password@db/dbname")
engine = create_async_engine(DATABASE_URL, echo=True)
metadata = MetaData()

async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)
