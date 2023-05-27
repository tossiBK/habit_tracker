import fire
from crud import Crud
from tracking import Tracking
from analytics import Analytics
from database import Database
from model.Habit import Habit, PeriodicityTypes
from model.HabitPerformanceTracking import HabitPerformanceTracking

from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta


class Internal_Habit():
    """
    Group for for the basic CRUD functions.

    Allows to create, readd (show), update and delete a habit.
    """
    def add(self, name, periodicity, note = None):
        """
        adds a new habit.

        Parameters
        ----------
        name : str
           name for the new habit
        periodicity : str
           sets the interval in which the habit is planed to be performed. allwoed values: 'd' (daily), 'w' (weekly), 'm' (monthly)
        note : str, optional
           an optional note for the habit.
        """
        # check input
        periodicityType = None

        match periodicity:
            case "d":
               periodicityType = PeriodicityTypes.DAY
            case "w":
                periodicityType = PeriodicityTypes.WEEK
            case "m":
                periodicityType = PeriodicityTypes.MONTH
            case _:
                return "input for periodicity was not valid. allowed values 'd', 'w', 'm'"
            
        crud = Crud()
        result = crud.add_habit(name, periodicityType, note)

        if type(result ) is Habit:
            return "Habit successfully added"

        match result:
            case -2:
                return "note must be a string"
            case -5:
                return "habit name is already in use"
            case _:
                return "Unknonw status was returned"

        
    
    def delete(self, habit_id):
        """
        deletes a habit.

        Parameters
        ----------
        habit_id : int
            id of the habit a to be deleted
        """
        crud = Crud()
        result = crud.delete_habit(habit_id)

        match result:
            case 1:
                return f"habit with id: {habit_id} successfully deleted"
            case -1:
                return f"no habit found for id: {habit_id}"
            case _:
                return "Unknonw status was returned"

    
    def pause(self, habit_id):
        """
        pause a habit (set inactive).

        Parameters
        ----------
        habit_id : int
            id of the habit a to be set pause (inactive)
        """
        crud = Crud()
        result = crud.activate_habit(habit_id, False)

        match result:
           case 1:
               return f"habit with id: {habit_id} successfully paused"
           case -1:
               return f"no habit found for id: {habit_id}"
           case _:
               return "Unknonw status was returned"
    
    def unpause(self, habit_id):
        """
        unpause a habit (set active).

        Parameters
        ----------
        habit_id : int
            id of the habit a to be set unpaused (active)
        """
        crud = Crud()
        result = crud.activate_habit(habit_id, True)

        match result:
           case 1:
               return f"habit with id: {habit_id} successfully unpaused"
           case -1:
               return f"no habit found for id: {habit_id}"
           case _:
               return "Unknonw status was returned"
    
    def update(self, habit_id, name=None, note=None):
        """
        updates a habit with the new given name and note. At least one of the two optional fields must have a value.

        Parameters
        ----------
        habit_id : int
            id of the habit to update
        name : str, optional
            new name for the habit to set. need to be unique
        note : str, optional
            new note for the habit to set. 
        """
        crud = Crud()
        result = crud.update_habit(habit_id, name, note)

        match result:
            case 1:
                return f"habit with id: {habit_id} successfully updated"
            case -1:
                return f"no habit found for id: {habit_id}"
            case -2:
                return "no values added to change, at least one must be submitted"
            case -3:
                return "habit name is already in use"
            case _:
                return "Unknonw status was returned"

       
    
    def show(self, habit_id):
        """
        shows a habit details for the provided habit id.

        Parameters
        ----------
        habit_id : int
            id of the habit to show
        """
        crud = Crud()
        result = crud.get_habit(habit_id)

        if result == -1:
            return f"no habit found for id: {habit_id}"

        output = f"name:\t{result.name}\n" \
            f"note:\t{result.note}\n" \
            f"periodicity:\t{result.periodicity}\n" \
            f"created:\t{result.created}\n" \
            f"active:\t{result.active}\n"
            
        
        return output


class Internal_Tracking():
    """
    Group for adding a tracking to a habit.

    Tracks a habit performance.
    """
    def add(self, habit_id, date=None):
        """
        Adds a tracking to a given habit. For the habit identification, the id of the habit is used.

        Parameters
        ----------
        habit_id : int
            id of the habit a tracking will be added
        date : str, optional, default: now()
            an optional date string in the following format 'yyyy-mm-dd hh:mm:ss'. If not provided it will use the actual date
        """
        tracking = Tracking()
        result = tracking.add(habit_id, date)

        match result:
            case 1:
                return f"Success: tracking was added for habit: {habit_id}"
            case -1:
                return f"no habit found for id: {habit_id}"
            case -2:
                return "Error, wrong date format. Use: yyyy-mm-dd hh:mm:ss"
            case _:
                return "Unknonw status was returned"

    


class Internal_Analytics():
    """
    Group for for showing analytics and statistics of the habits.

    Allows to view the different available statistics and analyses of the habits and their streaks.
    """
    def show_all(self, active=True):
        """
        Shows all habits registered. By default it shows the active habits, but can be changed to show the inactive habits by the optional parameter.

        Parameters
        ----------
        active : bool, optional, default: True
            optional flag to show all inactive habits, instead of the active habits (if set to False)
        """
        analytics = Analytics()

        data = analytics.get_all_habits(active)

        if data == -1:
            return "enetred optional parameter must be a bool value (True, False)"

        # if list is empty add a note.
        if len(data) == 0:
            return "No items found"


        # all okay, output the results
        output = f"Id\tName\n"
        
        for habit in data:
            output += f"{habit.id}\t{habit.name}\n"

        return output
    
    def show_by_periodicity(self, periodicity):
        """
        Shows all habits for a chosen period. 

        Parameters
        ----------
        periodicity : str
            identifier for the habits period to be shown. allowed values 'd', 'w', 'm'
        """

        periodicityType = None

        match periodicity:
            case "d":
               periodicityType = PeriodicityTypes.DAY
            case "w":
                periodicityType = PeriodicityTypes.WEEK
            case "m":
                periodicityType = PeriodicityTypes.MONTH
            case _:
                return "input for periodicity was not valid. allowed values 'd', 'w', 'm'"

        analytics = Analytics()

        data = analytics.get_all_habits_by_periodicity(periodicityType)

        # if list is empty add a note.
        if len(data) == 0:
            return "No items found"

        # all okay, output the results
        output = f"Id\tName\n"
        for habit in data:
            output += f"{habit.id}\t{habit.name}\n"

        return output
    
    def show_streaks(self, habit_id=None):
        """
        Shows the streaks for all active habits. Can be limited to a certain habit by providing the optional habit_id.

        Parameters
        ----------
        habit_id : int, optional, default: None
            filter for only showing the the selected habit
        """
        analytics = Analytics()

        data = analytics.get_longest_streak(habit_id)

        # if list is empty add a note.
        if len(data) == 0:
            return "No items found"

        # all okay, output the results
        output = f"Id\tName - longest streak\n"
        for habit in data:
            output += f"{habit.id}\t{habit.name} - streak: {habit.streak}\n"

        return output

class Demo():
    """
    Group for generating demo data.

    Adds a set of demo data to the app. Attention: This will delete all data!!
    It will add 6 habits, 2 daily, 2 weekly and 1 monthly. Each of the daily and weekly will have a full streak over 4 weeks and one will have gaps in it, 
    so the streaks are not over the whole time of tracking. The monthly will have one active and one inactive habit.
    """

    def generate(self):
        """
        Generates a set of demo data to use. ATTENTION: this will delete all current data!
        """
        # delete old dataset
        db = Database()
        db.reset_database()
        crud = Crud()
        tracking = Tracking()

        # we will use the date 1 month ago from generating the data, so we can use the data today
        creation_date = datetime.now() - relativedelta(months=1)

        # create all 6 habits
        habit_daily_1 = crud.add_habit("Daily Demo Habit 1", PeriodicityTypes.DAY, note="daily habit with a full streak over 4 weeks", date=creation_date)
        habit_daily_2 = crud.add_habit("Daily Demo Habit 2", PeriodicityTypes.DAY, note="daily habit with gaps over 4 weeks", date=creation_date)
        habit_weekly_1 = crud.add_habit("Weekly Demo Habit 1", PeriodicityTypes.WEEK, note="weekly habit with a full streak over 4 weeks", date=creation_date)
        habit_weekly_2 = crud.add_habit("Weekly Demo Habit 2", PeriodicityTypes.WEEK, note="weekly habit with gaps over 4 weeks", date=creation_date)
        habit_monthly_1 = crud.add_habit("Monthly Demo Habit 1", PeriodicityTypes.MONTH, note="monthly active demo habit", date=creation_date)
        habit_monthly_2 = crud.add_habit("Monthly Demo Habit 2", PeriodicityTypes.MONTH, note="monthly inactive demo habit", date=creation_date, active=False)

        # loop over 28 days = 4 weeks
        for i in range(28):
            cal_date = creation_date + timedelta(days=i)
            tracking.add(habit_daily_1.id, cal_date)

            # don´t add a tracking every 7 days
            if i % 7 != 0:
                tracking.add(habit_daily_2.id, cal_date)

        # loop over 4 weeks
        for i in range(4):
            cal_date = creation_date + timedelta(weeks=i)
            tracking.add(habit_weekly_1.id, cal_date)

            # don´t add a tracking every 2 weeks
            if i % 2 != 0:
                tracking.add(habit_weekly_2.id, cal_date)
        

        # for the month add one initial tracking after 1 hour
        tracking.add(habit_monthly_1.id, creation_date + timedelta(hours=1))

        return "demo dataset created."




class Cli():
    """
    Habit Tracker App. 
    
    The CLI tool offers all options for a simple and convienient interaction with the backand, to add, track and alalyze habits.
    It offers 3 module groups to interact. 
    """
    def __init__(self):
        self.tracking = Internal_Tracking()
        self.habit = Internal_Habit()
        self.analytics = Internal_Analytics()
        self.demo = Demo()
    
if __name__ == '__main__':
    """
    hook that loads only if this script is called but not included. Binds the CLI class to fire library.
    """
    fire.Fire(Cli)