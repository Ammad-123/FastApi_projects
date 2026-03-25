
from celery import Celery

REDIS_URL = "redis://redis:6379/0"

celery_app = Celery(
    "worker",
    broker=REDIS_URL,
    backend=REDIS_URL,
)