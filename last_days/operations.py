from datetime import datetime

from dateutil.relativedelta import relativedelta
from sqlalchemy.orm import Session

from last_days import models
from last_days import schemas


def get_notice_period_details(db: Session, date_of_resign,
                              notice_period_days, employee):

    if not employee and not date_of_resign:
        return {"data": {"message": "Employee name or date of resignation required"}}

    if employee and not date_of_resign:
        try:
            no_period = db.query(models.NoticePeriod).filter(models.NoticePeriod.employee.contains(employee)).first()
            lwd = no_period.date_of_resignation.date() + relativedelta(days=no_period.notice_period_days)
            days_remaining = (lwd - datetime.today().date()).days
            no_period.no_days_remaining = days_remaining
            no_period.lwd = lwd

            return no_period

        except:
            return {"employee": "employee does not exist. Please create record"}

    date = datetime.strptime(date_of_resign, "%Y-%m-%d")
    lwd = date.date() + relativedelta(days=notice_period_days)
    days_remaining = lwd - datetime.today().date()

    return {
        "lwd": lwd,
        "days_remaining": days_remaining.days,
        "notice_period": notice_period_days
    }


def get_notice_period_list(db: Session):
    all_notice_periods = db.query(models.NoticePeriod).all()  # all objects from table
    if all_notice_periods:
        return all_notice_periods
    

def add_notice_period(db: Session, np: schemas.NoticePeriodCreate):
    lwd = np.date_of_resignation + relativedelta(days=np.notice_period_days)

    if lwd >= datetime.today().date():
        days_remaining = (lwd - datetime.today().date()).days

        no_period = models.NoticePeriod(date_of_resignation=np.date_of_resignation,
                                        employee=np.employee, notice_period_days=np.notice_period_days)

        db.add(no_period)
        db.commit()  # commit changes so that object will be created in table
        db.refresh(no_period)
        no_period.message = "chotu chya aaichi gand"
        no_period.lwd = lwd
        no_period.no_days_remaining = days_remaining

        return no_period
    else:
        return {"employee": np.employee, "date_of_resignation": np.date_of_resignation,
                "message": "Niakal gaya bhidu khatam!!!"}


def delete_notice_period(db: Session, id: int):
    no_period = db.query(models.NoticePeriod).filter(models.NoticePeriod.id == id).first()
    db.delete(no_period)  # to remove record from table
    db.commit()

    return {"message": "Chutya... chandu zala tuza...bhk!!!!!"}


def update_notice_period(db: Session, id: int, np: schemas.NoticePeriod):
    no_period = db.query(models.NoticePeriod).filter(models.NoticePeriod.id == id).first()
    if no_period:
        if np.date_of_resignation:
            no_period.date_of_resignation = np.date_of_resignation
        
        if np.employee:
            no_period.employee = np.employee
        
        if np.no_days_remaining:
            no_period.no_days_remaining = np.no_days_remaining

        db.commit()
        db.refresh(no_period)

        return no_period
    else:
        return {"NoticePeriod": "Paper tak lvkr ethe entry nahiye tuzi lodu!!"}
