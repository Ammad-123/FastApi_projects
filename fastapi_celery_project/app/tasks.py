
from config import celery_app
import time

@celery_app.task(bind=True)
def long_task(self, data):
    """
    Simulates a long-running task
    """
    print(f"Processing data: {data}")
    for i in range(5):
        print(f"Step {i+1}/5")
        time.sleep(1)  # Simulate processing
    result = f"Processed {data} successfully!"
    print(result)
    return result