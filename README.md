# FastAPI JWT Authentication Project

**Learning project** built with FastAPI and JWT authentication.  
Purpose: to practice FastAPI, Pydantic, async database operations, and JWT-based authentication.

---

## Features

- User registration: `POST /users/register`
- Login and obtain JWT: `POST /users/login`
- Protected endpoint: `GET /protected_resource` (JWT required)

---

## Technologies

- Python 3.11+
- FastAPI
- SQLAlchemy + databases
- PyJWT
- passlib (bcrypt)
- Poetry for dependency management

---

## How to Run

1. Install dependencies with Poetry:
```bash
poetry install```
2. Activate the virtual environment created by Poetry (optional):
```bash
poetry shell```
3. Run the FastAPI server:
```bash
uvicorn main:app --reload```

4. API documentation and testing via Swagger UI:

http://127.0.0.1:8000/docs

---

## Notes
- SECRET_KEY is generated at app startup (acceptable for learning purposes).
- Passwords are stored hashed (bcrypt).
- JWT token is valid for 3 minutes (configurable in services.py).

---

## Project Structure
main.py
database.py
models.py
schemas.py
routers.py
crud.py
services.py


Each file has its responsibility: routers, models, Pydantic schemas, database operations, and service logic.
