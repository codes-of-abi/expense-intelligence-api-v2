# Expense Intelligence API

FastAPI + PostgreSQL + SQLAlchemy service to track expenses and get spending insights.

## Setup (PowerShell)

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env   # then put your real expense_admin password in .env
uvicorn app.main:app --reload
```

Open http://127.0.0.1:8000/docs for interactive Swagger docs.

## Endpoints

| Method | Path | Purpose |
|---|---|---|
| GET | `/health`, `/health/db` | App and database health |
| POST/GET | `/categories` | Create / list categories |
| POST/GET | `/expenses` | Create / list (filters: `category_id`, `start_date`, `end_date`, `min_amount`, `max_amount`, `search`, `skip`, `limit`) |
| GET/PATCH/DELETE | `/expenses/{id}` | Read / update / delete |
| GET | `/analytics/summary` | Count, total, average |
| GET | `/analytics/by-category` | Totals and share % per category |
| GET | `/analytics/monthly` | Totals per month |
| GET | `/analytics/top?limit=5` | Largest expenses |

Analytics endpoints accept optional `start_date` / `end_date`.

## Structure

```
app/
  main.py          # app, lifespan, router wiring
  config.py        # settings from .env (DATABASE_URL)
  database.py      # engine, SessionLocal, Base, get_db
  models.py        # Category, Expense
  schemas.py       # Pydantic schemas (DRF serializers equivalent)
  routers/         # categories, expenses, analytics (DRF viewsets equivalent)
  services/        # analytics queries
```

## Month 2 retrofit

Alembic migrations, JWT auth, pytest suite, error handling.
