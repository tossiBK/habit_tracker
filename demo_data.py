from database import Database
from tracking import Tracking
from crud import Crud

from model.Habit import PeriodicityTypes


from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta


class DemoData():
    """
    Class for generating a set of testing data for the unit tests and the user. 

    Methods
    -------
    generate()
        generates a set of habits and trackings. Can be used to offer the users an initial dataset to experiemtn with or for the unit testing.
    empty_db()
        resets the database to be in an empty initial state.
    """

    def generate(self):
        """
        Generates a set of data. It uses the actual month -1 month to start the entry for the habits and trackings. It creates 6 habits, each 2 for daily, weekly and monthly. 
        For the daily and weekly, one will have a full set of trackings to provide a streak, one will have gaps inside, to show the streaks calculation.
        For the monthly entries, one will be normal with an entry. The second habit is deactivated, to show this feature.
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

    def empty_db(self):
        """
        Resets the database to an empty state. Can be used to offer a clean DB reset for the end user.
        """
        db = Database()
        db.reset_database()