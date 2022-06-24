from datetime import date
from pydantic import BaseModel
from typing import Optional


class NoticePeriodBaseSchema(BaseModel):
    employee: str
    date_of_resignation: date
    lwd: Optional[date]
    no_days_remaining: Optional[int]
    message: Optional[str]
    notice_period_days: Optional[int]


class NoticePeriod(NoticePeriodBaseSchema):
    id: int

    class Config:
        orm_mode = True


class NoticePeriodCreate(NoticePeriodBaseSchema):

    class Config:
        orm_mode = True


class NoticePeriodUpdate(BaseModel):

    __annotations__ = {k: Optional[v] for k, v in NoticePeriodBaseSchema.__annotations__.items()}

    class Config:
        orm_mode = True


class RetrieveRemainingDays(BaseModel):

    no_days_remaining: int

    class Config:
        orm_mode = True
