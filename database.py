from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound, IntegrityError, OperationalError
from model.Habit import Habit
from model.Base import Base


# from datetime import datetime

class NotFoundException(Exception):
    "No result for the query was found"

class Database():
    """
    ORM handle for the database communication.


    Methods
    -------
    commit()
        commits the changes done to the session
    get_habits(active=None)
        returns a list of all habits from the database
    get_habits_by_periodicity(periodicity)
        returns a list of habits filtered by the periodicity from the database
    get_habit(id)
        fetches a habit by the id from the database
    add_habit(habit):
        writes a habit to the databse.
    delete_habit(habit)
        deletes the habit from the database
    """

    def __init__(self):
        """
        Constructor which initiales the engine and sessions used for the ORM to connect to the database.
        """
        self.engine = create_engine(f'sqlite:///habit_db.db', echo=False)
        self.session = Session(self.engine, expire_on_commit=False)
        self.__create_empty_db()
    
    def __create_empty_db(self):
        """
        Private functions, which checks if the table exist at the startup. If not existent, creates it.
        """
        try:
            # check if table for the object exists
            stmt = select(Habit)
            self.session.execute(stmt)
        except OperationalError:
            # don´t exists. run script for add the schema
            Base.metadata.create_all(self.engine)


    def commit(self):
        """
        commits the actual sessions changes to the database.

        Returns
        -------
        status_code : int
            returns the status code of the success of the commit.
             1: success
            -1: IntegrityError (e.g. failed unique contraint)
            -99: general (unchecked) db problem 
        """
        try:
            self.session.commit()

            return 1
        except IntegrityError:
            return -1
        except:
            return -99


    def get_habits(self, active=None):
        """
        returns the list of habits from the db.

        Parameters
        ----------
        active : bool, optional
            optional flag to filter by the active state (True / False)

        Returns
        -------
        habits : List<Habit>
            returns the list of the habits. Empty list if none found.
        """
        if active is not None:
            stmt = select(Habit).where(Habit.active == active)
        else:
             stmt = select(Habit)
        
        return self.session.execute(stmt).scalars().all()
    
    def get_habits_by_periodicity(self, periodicity):
        """
        returns the list of habits from the db.

        Parameters
        ----------
        periodicity : PeriodicityTypes
            perodicity for which the habits should be filtered

        Returns
        -------
        habits : List<Habit>
            returns the list of the habits. Empty list if none found.
        """
        stmt = select(Habit).where(Habit.periodicity == periodicity)

        return self.session.execute(stmt).scalars().all()
    
    def get_habit(self, id):
        """
        returns the habit for the provided id.

        Parameters
        ----------
        id : int
            id of the habit to be returned

        Returns
        -------
        habits : Habit or None
            returns tthe habit if found, otherwise None
        """
        try:
            stmt = select(Habit).where(Habit.id == id)
            result = self.session.execute(stmt).scalars().one()

            return result
        except NoResultFound:
            return None
    
    def add_habit(self, habit):
        """
        adds a given habit to the db.

        Parameters
        ----------
        habit : Habit
            item which should be added to the database

        Returns
        -------
        status_code : int
            status of the commit to the database
             1: success
            -1: duplicate name
            -99: general (unchecked) db problem 
        """
        try:
            self.session.add(habit)
            self.session.commit()

            return 1
        except IntegrityError:
            return -1
        except:
            return -99
        
    def delete_habit(self, habit):
        """
        deletes a given habit from the db.

        Parameters
        ----------
        habit : Habit
            item which should be deleted from the database

        Returns
        -------
        status_code : int
            status of the commit to the database
             1: success
            -99: general (unchecked) db problem 
        """
        try:
            self.session.delete(habit)
            self.session.commit()

            return 1
        except:
            return -99
        
    def reset_database(self):
        """
        drops all the data in the database and creates it new. Use with caution!
        """
        Base.metadata.drop_all(self.engine)
        Base.metadata.create_all(self.engine)
