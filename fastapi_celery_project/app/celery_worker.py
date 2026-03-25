from config import celery_app


import tasks

if __name__ == "__main__":
    celery_app.worker_main(argv=['worker', '--loglevel=info', '--pool=solo'])