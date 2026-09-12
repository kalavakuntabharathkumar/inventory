# Real-Time Inventory Sync API for Multi-Warehouse Retail

FastAPI + PostgreSQL + Redis inventory service with concurrency-safe stock updates, caching, tests, Docker, and GitHub Actions.

## Run locally

1. Copy `.env.example` to `.env`.
2. Start services:
   ```bash
   docker compose up --build
   ```
3. API docs: `http://localhost:8000/docs`

## Test

```bash
pip install -r requirements.txt
pytest --cov=app --cov-report=term-missing
```

The project includes an in-memory fallback for local/unit testing, while the Docker setup uses PostgreSQL and Redis.
