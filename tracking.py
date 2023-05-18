
from database import Database
# from model.Habit import Habit
from model.HabitPerformanceTracking import HabitPerformanceTracking
from datetime import datetime

class Tracking():

    def add(self, habit_id, date=None):
        """
            Adds a tracking to an existing habit.

            :param id of the habit to add a tracking
            :param a date in the format yyyy-mm-dd hh:mm:ss for adding a different time for the tracking than now (default: now, optional)
            :return bool status
        
        """
        # check if id is a number
        if type(habit_id) is not int:
            return "Error, not a valid integer"
        
        # check if date is in the correct format
        formatted_date = None
        if date is not None:
            try:
               formatted_date =  datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
            except ValueError:
                return "Error, wrong date format. Use: yyyy-mm-dd hh:mm:ss"


        database = Database()

        # check the id and test if the habit exists
        habit = database.get_habit(habit_id)

        if habit is None:
            return "Error, not found"
        
        
        # # create the new tracking
        t_entry = HabitPerformanceTracking()
        if formatted_date is not None:
            t_entry.track_date = formatted_date

        habit.tracking.append(t_entry)
        database.commit()

        return {'code': 1, 'msg': "Success"}
        