from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound, IntegrityError


from model.Habit import Habit, PeriodicityTypes
from model.HabitPerformanceTracking import HabitPerformanceTracking
from model.Base import Base


# from datetime import datetime

class NotFoundException(Exception):
    "No result for the query was found"

class Database():
    """
    ORM handle for the database communication.


    """

    def __init__(self):
        self.engine = create_engine(f'sqlite:///db1.db', echo=True)
        self.session = Session(self.engine)
    
    def commit(self):
        try:
            self.session.commit()

            return {'code': 1, 'msg': 'success'}
        except IntegrityError:
            return {'code': -1, 'msg': 'duplicate name'}
        except:
            return {'code': -99, 'msg': 'general error'}


    def get_habits(self, active=None):
        habits = []
        if active is not None:
            stmt = select(Habit).where(Habit.active == active)
        else:
             stmt = select(Habit)
        
        return self.session.execute(stmt).scalars().all()
    
    def get_habits_by_periodicity(self, periodicity):
        stmt = select(Habit).where(Habit.periodicity == periodicity)

        return self.session.execute(stmt).scalars().all()
    
    def get_habit(self, id):
        try:
            stmt = select(Habit).where(Habit.id == id)
            result = self.session.execute(stmt).scalars().one()

            return result
        except NoResultFound:
            return None
        # else:
        #     if result is None:
        #         raise NotFoundException
        #     else:
        #         return result
    
    def add_habit(self, habit):
        try:
            self.session.add(habit)
            self.session.commit()

            return {'code': 1, 'msg': 'success'}
        except IntegrityError:
            return {'code': -1, 'msg': 'duplicate name'}
        except:
            return {'code': -99, 'msg': 'general error'}

        
    def delete_habit(self, habit):
        try:
            self.session.delete(habit)
            self.session.commit()

            return {'code': 1, 'msg': 'success'}
        except IntegrityError:
            return {'code': -1, 'msg': 'duplicate name'}
        except:
            return {'code': -99, 'msg': 'general error'}



# with Session(engine) as session:
#     habit = Habit(name="Test", periodicity=PeriodicityTypes.DAY)

#     session.add(habit)
#     session.commit()

# print(habit)

# Base.metadata.create_all(engine)

# session = Session(engine)

# stmt = select(HabitPerformanceTracking)

# for habit in session.scalars(stmt):
#     habit.tracking.append(HabitPerformanceTracking())
#     session.commit()

# stmt = select(HabitPerformanceTracking)
# for habit in session.scalars(stmt):
#     print(habit)
    


