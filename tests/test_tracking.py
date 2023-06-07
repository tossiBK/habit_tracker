# for unit tests to be available in a subfolder, to avoid package and module errors we must do add the absolute path
# to our root folder, where the files to import are located
import sys
import os
 
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from analytics import Analytics
from database import Database
from model.Habit import Habit, PeriodicityTypes
from tracking import Tracking
from datetime import datetime
import pytest

# import datetime

# set environment for test to use correct DB
os.environ["UNITTEST"] = "1"

def test_init():
    # reset db so we have a clear unit set to test in stand alone
    database = Database()
    database.reset_database()

def test_add():
    # # reset db so we have a clear unit set to test in stand alone
    database = Database()
    
    # create a habit where we can add the tracking
    habit = Habit()
    habit.name = "test habit tracking"
    habit.periodicity = PeriodicityTypes.DAY
    database.add_habit(habit)

    tracking = Tracking()

    # check minimum parameter
    with pytest.raises(TypeError):
        tracking.add()

    # check failure of not sending a integer id
    assert tracking.add("") == -1

    # check wrong date format
    assert tracking.add(1, "") == -2

    # check failure for not existing habit id
    assert tracking.add(-1) == -3

    # check adding was succesful for an entry now
    assert tracking.add(habit.id) == 1

    # check adding was succesful for an entry now
    assert tracking.add(habit.id, datetime.now()) == 1
    