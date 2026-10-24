from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db

router = APIRouter(prefix="/categories", tags=["categories"])


@router.post("", response_model=schemas.CategoryRead, status_code=status.HTTP_201_CREATED)
def create_category(payload: schemas.CategoryCreate, db: Session = Depends(get_db)):
    name = payload.name.strip()
    if db.scalar(select(models.Category).where(models.Category.name == name)):
        raise HTTPException(status.HTTP_409_CONFLICT, "Category already exists")
    category = models.Category(name=name)
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


@router.get("", response_model=list[schemas.CategoryRead])
def list_categories(db: Session = Depends(get_db)):
    return db.scalars(select(models.Category).order_by(models.Category.name)).all()
