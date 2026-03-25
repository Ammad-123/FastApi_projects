
from fastapi import FastAPI, BackgroundTasks
from tasks import long_task

app = FastAPI(title="FastAPI + Celery Queue")

@app.get("/")
def read_root():
    return {"message": "Hello! FastAPI is running with Celery queue."}

@app.post("/process/{data}")
def process_data(data: str):
    """
    Send a long-running task to Celery
    """
    task = long_task.delay(data)
    return {"task_id": task.id, "status": "Processing in background"}

@app.get("/status/{task_id}")
def get_status(task_id: str):
    """
    Check the status of a background task
    """
    from config import celery_app
    res = celery_app.AsyncResult(task_id)
    return {"task_id": task_id, "status": res.status, "result": res.result}