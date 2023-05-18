from database import Database
from model.Habit import PeriodicityTypes
# from model.HabitPerformanceTracking import HabitPerformanceTracking

from datetime import timedelta#, datetime

class Analytics():

    def show_all_habits(self, active=True):
        
        database = Database()

        habits = database.get_habits(active)
        return habits

    def show_all_habits_by_periodicity(self, periodicity):
        # check input

        periodicityType = None

        match periodicity:
            case "d":
               periodicityType = PeriodicityTypes.DAY
            case "w":
                periodicityType = PeriodicityTypes.WEEK
            case "m":
                periodicityType = PeriodicityTypes.MONTH
            case __:
                #throw error
                pass

        database = Database()

        habits = database.get_habits_by_periodicity(periodicityType)
        return habits
    
    def show_longest_streak(self, habit_id=None):
        # check input

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

            print(habit.periodicity.value)

            for tracking in habit.tracking:
                if previous is None:
                    previous = tracking.track_date
                    continue


                keep_stroke = self.__compareDates(previous, tracking.track_date, habit.periodicity.value)

                previous = tracking.track_date
                i += 1

                # compare them
                if keep_stroke == False:
                    if longest < i:
                        longest = i
                    i = 0
            
            # make a temporary member to add the longest calculated streak, but not saving it to the database
            habit.streak = longest

        return habits
    
    def __compareDates(self, date1, date2, interval):
        match interval:
            case 'd':
                previous = date1 + timedelta(days=1)
                day_of_month_prev = int(previous.strftime("%d"))
                
                day_of_month_act = int(date2.strftime("%d"))
                return day_of_month_prev == day_of_month_act
            case 'w':
                previous = date1 + timedelta(week=1)
                week_of_year_prev = int(previous.strftime("%W"))
                
                week_of_year_act = int(date2.strftime("%W"))
                return week_of_year_prev == week_of_year_act
            case 'm':
                previous = date1 + timedelta(month=1)
                month_of_year_prev = int(previous.strftime("%m"))
                
                month_of_year_act = int(date2.strftime("%m"))
                return month_of_year_prev == month_of_year_act


