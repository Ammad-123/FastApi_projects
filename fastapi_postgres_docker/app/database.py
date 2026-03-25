from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import time
import os

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgres@db:5432/fastapi_db"
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# wait for DB
def wait_for_db():
    retries = 10
    while retries:
        try:
            engine.connect()
            return
        except Exception:
            print("Waiting for database...")
            time.sleep(2)
            retries -= 1
    raise Exception("Database not ready")


wait_for_db()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()