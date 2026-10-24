from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app import models, schemas
from app.database import get_db

router = APIRouter(prefix="/expenses", tags=["expenses"])


def _ensure_category(db: Session, category_id: int | None) -> None:
    if category_id is not None and db.get(models.Category, category_id) is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"Category {category_id} not found")


def _get_or_404(db: Session, expense_id: int) -> models.Expense:
    expense = db.get(models.Expense, expense_id)
    if expense is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Expense not found")
    return expense


@router.post("", response_model=schemas.ExpenseRead, status_code=status.HTTP_201_CREATED)
def create_expense(payload: schemas.ExpenseCreate, db: Session = Depends(get_db)):
    _ensure_category(db, payload.category_id)
    expense = models.Expense(**payload.model_dump())
    db.add(expense)
    db.commit()
    db.refresh(expense)
    return expense


@router.get("", response_model=list[schemas.ExpenseRead])
def list_expenses(db: Session = Depends(get_db)):
    stmt = (
        select(models.Expense)
        .options(joinedload(models.Expense.category))
        .order_by(models.Expense.expense_date.desc(), models.Expense.id.desc())
    )
    return db.scalars(stmt).all()


@router.get("/{expense_id}", response_model=schemas.ExpenseRead)
def get_expense(expense_id: int, db: Session = Depends(get_db)):
    return _get_or_404(db, expense_id)


@router.patch("/{expense_id}", response_model=schemas.ExpenseRead)
def update_expense(expense_id: int, payload: schemas.ExpenseUpdate, db: Session = Depends(get_db)):
    expense = _get_or_404(db, expense_id)
    changes = payload.model_dump(exclude_unset=True)
    if "category_id" in changes:
        _ensure_category(db, changes["category_id"])
    for field, value in changes.items():
        setattr(expense, field, value)
    db.commit()
    db.refresh(expense)
    return expense


@router.delete("/{expense_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_expense(expense_id: int, db: Session = Depends(get_db)):
    db.delete(_get_or_404(db, expense_id))
    db.commit()
