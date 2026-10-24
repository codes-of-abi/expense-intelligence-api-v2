from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI
from sqlalchemy import text
from sqlalchemy.orm import Session

from app import models  # noqa: F401  (registers tables on Base)
from app.database import Base, engine, get_db
from app.routers import categories


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)  # Alembic migrations come in Month 2
    yield


app = FastAPI(
    title="Expense Intelligence API",
    description="Track expenses and get spending insights.",
    version="0.1.0",
    lifespan=lifespan,
)


app.include_router(categories.router)


@app.get("/health", tags=["health"])
def health():
    return {"status": "ok"}


@app.get("/health/db", tags=["health"])
def health_db(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1"))
    return {"database": "connected"}
