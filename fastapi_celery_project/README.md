FastAPI + Celery + Redis Project

A fully working FastAPI backend with Celery for background task processing and Redis as the message broker. This project demonstrates:

Asynchronous background tasks using Celery
FastAPI REST API endpoints
Task status monitoring
Dockerized deployment for backend, worker, and Redis
Scalable and responsive API under concurrent load
Project Structure
fastapi_celery_project/
├── app/
│   ├── main.py            # FastAPI application
│   ├── tasks.py           # Celery tasks
│   ├── config.py          # Celery + Redis configuration
│   ├── celery_worker.py   # Worker entrypoint (imports tasks)
│   └── requirements.txt   # Python dependencies
├── Dockerfile             # Dockerfile for backend & worker
├── docker-compose.yml     # Docker Compose for backend, worker, Redis
└── README.md
Requirements
Python 3.12+
Docker & Docker Compose (for containerized setup)
Redis (optional if running locally without Docker)
Installation
1. Clone the repository
git clone
cd fastapi_celery_project
2. Build and run with Docker Compose
docker-compose up --build

This will start:

FastAPI backend: http://localhost:8000
Celery worker: processes background tasks
Redis: on port 6379
3. Install dependencies manually (optional)

If running locally without Docker:

pip install -r app/requirements.txt

Start services manually:

# Start Redis
redis-server

# Start FastAPI
uvicorn app.main:app --reload

# Start Celery worker
celery -A app.config.celery_app worker --loglevel=info
API Endpoints
1. Health Check
GET /

Response:

{
  "message": "Hello! FastAPI is running with Celery queue."
}
2. Submit a Background Task
POST /process/{data}

Example:

POST http://localhost:8000/process/hello

Response:

{
  "task_id": "c1f2d3e4-5678-90ab-cdef-1234567890ab",
  "status": "Processing in background"
}
3. Check Task Status
GET /status/{task_id}

Example:

GET http://localhost:8000/status/c1f2d3e4-5678-90ab-cdef-1234567890ab

Response:

{
  "task_id": "c1f2d3e4-5678-90ab-cdef-1234567890ab",
  "status": "SUCCESS",
  "result": "Processed hello successfully!"
}
Project Highlights
Background Tasks: Heavy or long-running tasks do not block API requests.
Scalability: Add more Celery workers to process tasks concurrently.
Dockerized: Easy deployment and reproducible environment.
Simple Monitoring: Task logs visible in Celery worker console.
Folder Notes
app/main.py → FastAPI REST API
app/tasks.py → Long-running task definitions
app/config.py → Celery + Redis setup
app/celery_worker.py → Only imports tasks (worker is run via Docker/CLI)
docker-compose.yml → Launches backend, worker, Redis together
Optional: Flower Monitoring

To monitor Celery tasks visually:

pip install flower
celery -A app.config.celery_app flower

Open Flower UI: http://localhost:5555

Client Demo Tips
Send multiple tasks quickly via /process/{data} to show FastAPI responsiveness.
Observe worker logs or Flower UI to see tasks being processed in background.
Show task results using /status/{task_id} endpoint.