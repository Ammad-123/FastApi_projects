# 🚀 FastAPI Docker PostgreSQL REST API

Production-ready FastAPI REST API with PostgreSQL, Docker, and clean architecture. This project demonstrates a simple backend service with database integration, modular structure, and containerized deployment.

---

# 📦 Features

* FastAPI REST API
* PostgreSQL database
* Docker + docker-compose
* SQLAlchemy ORM
* Clean project structure
* CRUD endpoints
* Swagger documentation
* Production-ready setup

---

# 🏗 Project Structure

```
fastapi-docker-api/
│
├── app/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── crud.py
│   └── routers/
│       └── items.py
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

# ⚙️ Requirements

* Docker
* Docker Compose

OR (without docker)

* Python 3.11+
* PostgreSQL

---

# 🚀 Run with Docker

## Build and start containers

```
docker-compose up --build
```

Run in background:

```
docker-compose up --build -d
```

Stop containers:

```
docker-compose down
```

Remove containers + volumes:

```
docker-compose down -v
```

---

# 🌐 API Access

Swagger UI:

```
http://localhost:8000/docs
```

ReDoc:

```
http://localhost:8000/redoc
```

---

# 📌 API Endpoints

## Create Item

POST /items

```
{
  "name": "Laptop",
  "description": "Macbook Pro"
}
```

## Get All Items

GET /items

## Get Single Item

GET /items/{id}

## Delete Item

DELETE /items/{id}

---

# 🗄 Database

PostgreSQL container runs on:

```
Host: localhost
Port: 5432
User: postgres
Password: postgres
Database: fastapi_db
```

Connection URL:

```
postgresql://postgres:postgres@db:5432/fastapi_db
```

---

# 🐳 Docker Services

## API Service

* FastAPI application
* Runs on port 8000
* Auto connects to database

## DB Service

* PostgreSQL 15
* Persistent volume
* Exposed port 5432

---

# 🧠 Tech Stack

* FastAPI
* Python
* PostgreSQL
* SQLAlchemy
* Docker
* Pydantic
* Uvicorn

---

# 🔧 Local Development (without Docker)

Install dependencies:

```
pip install -r requirements.txt
```

Run server:

```
uvicorn app.main:app --reload
```

---

# 📄 Example Response

```
[
  {
    "id": 1,
    "name": "Laptop",
    "description": "Macbook"
  }
]
```

---

# ✅ Project Scope

* 2–4 REST API endpoints
* PostgreSQL integration
* Clean architecture
* Docker setup
* Swagger documentation
* Production-ready code

---

# 👨‍💻 Author Role

FastAPI Backend Developer

* REST API design
* Database integration
* Docker containerization
* Clean code architecture
* Production-ready deployment

---

# 📜 License

This project is for demonstration and learning purposes.

---

# ⭐ Ready to Use

This project can be directly used as a starter template for:

* SaaS backend
* Microservices
* CRUD API
* Admin dashboard backend
* Mobile app backend
* AI service backend

---

Happy Coding 🚀
