from datetime import datetime
from sqlalchemy import (Column, Integer, String, DateTime) # noqa F403
from app.database import Base # noqa F403


class NoticePeriod(Base):
    __tablename__ = "noticeperiod"

    id = Column(Integer, primary_key=True, index=True)
    date_of_resignation = Column(DateTime, default=datetime.utcnow)
    employee = Column(String, index=True)
    notice_period_days = Column(Integer, index=True)


