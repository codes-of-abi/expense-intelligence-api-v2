from datetime import date
from decimal import Decimal

from sqlalchemy import extract, func, select
from sqlalchemy.orm import Session

from app.models import Category, Expense


def _date_filters(stmt, start_date: date | None, end_date: date | None):
    if start_date:
        stmt = stmt.where(Expense.expense_date >= start_date)
    if end_date:
        stmt = stmt.where(Expense.expense_date <= end_date)
    return stmt


def summary(db: Session, start_date: date | None, end_date: date | None) -> dict:
    stmt = _date_filters(
        select(func.count(Expense.id), func.coalesce(func.sum(Expense.amount), 0)),
        start_date,
        end_date,
    )
    count, total = db.execute(stmt).one()
    total = Decimal(total)
    average = (total / count).quantize(Decimal("0.01")) if count else Decimal("0.00")
    return {"count": count, "total": total, "average": average}


def by_category(db: Session, start_date: date | None, end_date: date | None) -> list[dict]:
    total_col = func.sum(Expense.amount)
    stmt = _date_filters(
        select(
            func.coalesce(Category.name, "Uncategorized"),
            func.count(Expense.id),
            total_col,
        ).select_from(Expense).outerjoin(Category, Expense.category_id == Category.id),
        start_date,
        end_date,
    ).group_by(Category.name).order_by(total_col.desc())
    rows = db.execute(stmt).all()
    grand_total = sum((Decimal(r[2]) for r in rows), Decimal("0"))
    return [
        {
            "category": name,
            "count": count,
            "total": Decimal(total),
            "share_percent": round(float(Decimal(total) / grand_total * 100), 1) if grand_total else 0.0,
        }
        for name, count, total in rows
    ]


def monthly(db: Session, start_date: date | None, end_date: date | None) -> list[dict]:
    year = extract("year", Expense.expense_date)
    month = extract("month", Expense.expense_date)
    stmt = _date_filters(
        select(year, month, func.sum(Expense.amount), func.count(Expense.id)),
        start_date,
        end_date,
    ).group_by(year, month).order_by(year, month)
    return [
        {"month": f"{int(y):04d}-{int(m):02d}", "total": Decimal(total), "count": count}
        for y, m, total, count in db.execute(stmt).all()
    ]


def top_expenses(db: Session, limit: int, start_date: date | None, end_date: date | None) -> list[Expense]:
    stmt = _date_filters(select(Expense), start_date, end_date)
    return list(db.scalars(stmt.order_by(Expense.amount.desc()).limit(limit)).all())
