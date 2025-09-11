from contextlib import asynccontextmanager

import databases
from fastapi import FastAPI
from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine


DATABASE_URL = "sqlite:///./users.sqlite"
Base = declarative_base()


def init_db():
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(engine)


database = databases.Database(DATABASE_URL)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    yield
    await database.disconnect()
