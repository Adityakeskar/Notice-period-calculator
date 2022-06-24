import datetime
from datetime import date

from dateutil.relativedelta import relativedelta
from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session
from typing import List, Union

from last_days import models, operations as ops, schemas
from app import database


models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()


def get_db():
    db = database.SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.post("/notice-period/", response_model=schemas.NoticePeriodCreate)
def notice_period_add(notice_period: schemas.NoticePeriodCreate, db: Session=Depends(get_db)):
    return ops.add_notice_period(db=db, np=notice_period)


@app.get("/notice-periods/", response_model=List[schemas.NoticePeriod])
def notice_period_list(db: Session=Depends(get_db)):
    return ops.get_notice_period_list(db)


@app.get("/notice-period/{id}/", response_model=schemas.NoticePeriod)
def notice_period_detail(id: int, db: Session=Depends(get_db)):
    return ops.get_notice_period_details(db=db, id=id)


@app.patch("/notice-period/{id}/change/", response_model=schemas.NoticePeriodUpdate)
def address_change(id: int, notice_period: schemas.NoticePeriodUpdate,
                   db: Session=Depends(get_db)):
    return ops.update_notice_period(db=db, id=id, np=notice_period)


@app.delete("/notice-period/{id}/delete/")
def notice_period_delete(id: int, db: Session=Depends(get_db)):
    return ops.delete_notice_period(db=db, id=id)


@app.get("/notice-period/")
def calculate_np(date_of_resign=None, notice_period_days: int = 60,
                 employee=None, db: Session=Depends(get_db)):
    return ops.get_notice_period_details(db=db, date_of_resign=date_of_resign,
                                         notice_period_days=notice_period_days,
                                         employee=employee)
