from fastapi import FastAPI
from .database import engine, Base
from .routers import items

Base.metadata.create_all(bind=engine)

app = FastAPI(title="FastAPI Docker API")

app.include_router(items.router)