from model.Base import Base 
from sqlalchemy import func

from typing import Optional
from typing import List
from sqlalchemy import String, Boolean

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from datetime import datetime
import enum

from model.HabitPerformanceTracking import HabitPerformanceTracking

class PeriodicityTypes(enum.Enum):
    """
    Enum for representing the options for the periodicity of a habit.

    Attributes
    ----------
    DAY: constant
        period for a daily habit
    WEEK: constant
        period for a weekly habit
    MONTH: constant
        period for a monthly habit
    """

    DAY = 'd'
    WEEK = 'w'
    MONTH = 'm'

class Habit(Base):
    """
    Mapped Model class for represnting an entity in the database for a habit. Relations (Tracking) 
    for the habut is included as a relationship mapping in this model class too.

    Attributes    
    ----------
    id : int
        id of the entry in the database. primary key, auto generated
    name : str
        name of the habit
    note : str
        (Optional) note for the habit. Can include any informational note the user may like for a habit (e.g. what to do, how to do, goal etc...)
    periodicity : PeriodicityTypes
        periodicity (interval) in which the habit must be tracked as performed to fulfil the mean of a habit
    created : datetime
        date when the habit was created. Optional as it will use the actual time at the time of the creation (default: now())
    active : bool
        flag if the habit was paused or is active at the moment. (default: true)
    tracking : list[HabitPerformanceTracking]
        list of all assigned trackings as performed for the habit
    """


    __tablename__ = "habits"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), unique=True)
    note: Mapped[Optional[str]]
    periodicity: Mapped[PeriodicityTypes] 
    created: Mapped[datetime] = mapped_column(insert_default=func.now())
    active: Mapped[bool] = mapped_column(Boolean, default=1)

    tracking: Mapped[List["HabitPerformanceTracking"]] = relationship(
        back_populates="habit", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"Habit(id={self.id!r}, name={self.name!r}, note={self.note!r}, periodicity={self.periodicity!r}, created={self.created!r}, active={self.active!r}, tracking={self.tracking!r})"