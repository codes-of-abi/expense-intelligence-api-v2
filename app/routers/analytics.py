from datetime import date

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app import schemas
from app.database import get_db
from app.services import analytics

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/summary")
def get_summary(start_date: date | None = None, end_date: date | None = None, db: Session = Depends(get_db)):
    return analytics.summary(db, start_date, end_date)


@router.get("/by-category")
def get_by_category(start_date: date | None = None, end_date: date | None = None, db: Session = Depends(get_db)):
    return analytics.by_category(db, start_date, end_date)


@router.get("/monthly")
def get_monthly(start_date: date | None = None, end_date: date | None = None, db: Session = Depends(get_db)):
    return analytics.monthly(db, start_date, end_date)


@router.get("/top", response_model=list[schemas.ExpenseRead])
def get_top(
    limit: int = Query(default=5, ge=1, le=50),
    start_date: date | None = None,
    end_date: date | None = None,
    db: Session = Depends(get_db),
):
    return analytics.top_expenses(db, limit, start_date, end_date)
