from database import Database
from datetime import timedelta
from dateutil.relativedelta import relativedelta

class Analytics():
    """
    Class provides all functions for analysing the habits for a certain criteria.

    Methods
    -------
    get_all_habits(active=True)
        collects all habits registered. By default all active habits, but can be changed to the inactive habits by the optional parameter.
    get_all_habits_by_periodicity(periodicity)
        collects all habits for a period. 
    get_longest_streak(habit_id=None)
        calculates the streaks for all active habits. Can be limited to a certain habit by providing the optional habit_id.
    """

    def get_all_habits(self, active=True):
        """
        Collects all habits registered. By default all active habits, but can be changed to the inactive habits by the optional parameter.

        Parameters
        ----------
        active : bool, optional, default: True
            optional flag to show all inactive habits, instead of the active habits (if set to False)

        Returns
        -------
        habits : List<Habit>
            returns the list of the habits. Empty list if none found. -1 if optional parameter was not a bool.
        """
        # check input if bool
        if type(active) is not bool:
            return -1

        database = Database()

        habits = database.get_habits(active)
        return habits

    def get_all_habits_by_periodicity(self, periodicity):
        """
        Collects all habits for a period. 

        Parameters
        ----------
        periodicity : PeriodicityTypes
            chosen periodicity for which the haiits will be selected
            

        Returns
        -------
        habits : List<Habit>
            returns the list of the habits. Empty list if none found.
        """
        database = Database()

        habits = database.get_habits_by_periodicity(periodicity)
        return habits
    
    def get_longest_streak(self, habit_id=None):
        """
        Calculates the streaks for all active habits. Can be limited to a certain habit by providing the optional habit_id.

        Parameters
        ----------
        habit_id : int, optional, default: None
            limits the results to a certain habit

        Returns
        -------
        habits : List<Habit>
            returns the list of the habits including the calculated streak member. Empty list if none found.
        """
        
        # check if id is a number
        if habit_id is not None and type(habit_id) is not int:
            return []

        # fetch the habits
        database = Database()

        if habit_id is not None:
            # if we only have one to fetch, add it to a list for the later iteration
            # so we can use the same code simply again
            habits = [database.get_habit(habit_id)]
        else:
            habits = database.get_habits()

        # calculate the streaks of each one and add it to the object        
        for habit in habits:
            i = 0
            longest = 0
            previous = None

            # iterate over all trackings and calculate if they run inside the desired period
            for tracking in habit.tracking:
                # first item won´t have a previous, so we don´t need to compare it
                if previous is None:
                    previous = tracking.track_date
                    i += 1
                    continue

                # compare the values and check if we still keep the streak
                keep_streak = self.__compareDates(previous, tracking.track_date, habit.periodicity.value)


                # if streak is broken, check if we have a longer one, if so add, and reset counter
                if keep_streak == False:
                    if longest < i:
                        longest = i
                    i = 0
            
                previous = tracking.track_date
                i += 1
            # check longest again after finishing the check, as it won´t be written otherwise if the streak was not broken
            # make a temporary member to add the longest calculated streak, but not saving it to the database
            if longest < i:
                longest = i
            habit.streak = longest

        return habits
    
    def __compareDates(self, date1, date2, interval):
        """
        compares 2 given dates if both are inside the same interval (consecutive)

        Parameters
        ----------
        date1 : datetime
            first date for the comparison
        date2 : datetime
            second date for the comparison
        interval : str
            interval for the check, values 'd', 'w', 'm'

        Returns
        -------
        result : bool
            returns True if both dates are inside the provided interval (consecutive)
        """

        match interval:
            case 'd':
                previous = date1 + timedelta(days=1)
                day_of_month_prev = int(previous.strftime("%d"))
                
                day_of_month_act = int(date2.strftime("%d"))
                return day_of_month_prev == day_of_month_act
            case 'w':
                previous = date1 + timedelta(weeks=1)
                week_of_year_prev = int(previous.strftime("%W"))
                
                week_of_year_act = int(date2.strftime("%W"))
                return week_of_year_prev == week_of_year_act
            case 'm':
                previous = date1 + relativedelta(months=1)
                month_of_year_prev = int(previous.strftime("%m"))
                
                month_of_year_act = int(date2.strftime("%m"))
                return month_of_year_prev == month_of_year_act


