from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from sqlalchemy import func

from model.Base import Base 
from datetime import datetime

class HabitPerformanceTracking(Base):
    """
    Model for the database table of the habit_performance_tracking.
    """

    __tablename__ = "habit_performance_tracking"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    habit_id: Mapped[int] = mapped_column(ForeignKey("habits.id"))
    track_date: Mapped[datetime] = mapped_column(insert_default=datetime.now())

   
    habit: Mapped["Habit"] = relationship(back_populates="tracking")


    def __repr__(self) -> str:
        return f"HabitPerformanceTracking(id={self.id!r}, habit_id={self.habit_id!r}, track_date={self.track_date!r})"