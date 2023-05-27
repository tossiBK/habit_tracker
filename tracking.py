
from database import Database
from model.HabitPerformanceTracking import HabitPerformanceTracking
from datetime import datetime

class Tracking():
    """
    Class for adding a tracking for the habits.

    Methods
    -------
    add(habit_id, date=None)
        adds the tracking for a given habit
    """

    def add(self, habit_id, date=None):
        """
         Adds a tracking to an existing habit.
        
        Parameters
        ----------
        habit_id : int
            id of the habit a tracking will be added
        date : datetime, optional, default: now()
            an optional datetime object to set a tracking at a specific time

        
        Returns
        -------
        status_code : int
            code if the tracking was added succesful, or a failure code in case of an error
             1: success
            -1: habit_id was not a positive integer
            -2: date was not from type datetime
            -3: no habit was found for the provided habit_id
        
        """
        # check if id is a number
        if type(habit_id) is not int:
            return -1
        
        # check if date is in the correct format
        if date is not None and type(date) is not datetime:
           return -2


        # check the id and test if the habit exists
        database = Database()
        habit = database.get_habit(habit_id)

        if habit is None:
            return -3
        
        # create the new tracking
        t_entry = HabitPerformanceTracking()
        if date is not None:
            t_entry.track_date = date

        habit.tracking.append(t_entry)
        database.commit()

        return 1