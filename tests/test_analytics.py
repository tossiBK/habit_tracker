# for unit tests to be available in a subfolder, to avoid package and module errors we must do add the absolute path
# to our root folder, where the files to import are located
import sys
import os
 
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from analytics import Analytics
from database import Database
from tracking import Tracking
from demo_data import DemoData
from model.Habit import PeriodicityTypes
import pytest

import datetime

# set environment for test to use correct DB
os.environ["UNITTEST"] = "1"

def test_init():
    # # reset db so we have a clear unit set to test in stand alone
    # database = Database()
    # database.reset_database()

    # create data set
    demo_data = DemoData()
    demo_data.generate()


def test_get_all_habits():
    # create data set
    demo_data = DemoData()
    demo_data.generate()

    analytics = Analytics()
    
    # check for correct appliance from optional parameter
    assert analytics.get_all_habits(active="") == -1

    # check the pre defined set for correct length of entries
    assert len(analytics.get_all_habits()) == 5
    assert len(analytics.get_all_habits(active=True)) == 5
    assert len(analytics.get_all_habits(active=False)) == 1

def test_get_all_habits_by_periodicity():
    analytics = Analytics()

    # check parameter amount
    with pytest.raises(TypeError):
        analytics.get_all_habits_by_periodicity()

    # assert empty array if none was entered
    assert analytics.get_all_habits_by_periodicity("") == []

    # assert the correct amount by our prefab data
    assert len(analytics.get_all_habits_by_periodicity(PeriodicityTypes.DAY)) == 2
    assert len(analytics.get_all_habits_by_periodicity(PeriodicityTypes.WEEK)) == 2
    assert len(analytics.get_all_habits_by_periodicity(PeriodicityTypes.MONTH)) == 2

def test_get_longest_streak():
    analytics = Analytics()

    # check if all was returned with the correct amount
    data = analytics.get_longest_streak()

    assert data[0].streak == 28
    assert data[1].streak == 6
    assert data[2].streak == 4
    assert data[3].streak == 1
    assert data[4].streak == 1
    assert data[5].streak == 0

    # check if pasting a wrong type result in empty response
    assert analytics.get_longest_streak(habit_id="") == []

    # check if pasting a wrong id result in empty response
    assert analytics.get_longest_streak(habit_id=-1) == []

    # check if one by id works
    data_one = analytics.get_longest_streak(habit_id=1)
    assert data_one[0].streak == 28
 