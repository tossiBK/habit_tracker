# for unit tests to be available in a subfolder, to avoid package and module errors we must do add the absolute path
# to our root folder, where the files to import are located
import sys
import os
 
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

import pytest
from model.Habit import Habit, PeriodicityTypes
from crud import Crud
from database import Database


# set environment for test to use correct DB
os.environ["UNITTEST"] = "1"

def test_init():
    # reset db so we have a clear unit set to test in stand alone
    database = Database()
    database.reset_database()

def test_add_habit():
    crud = Crud()
    
    # check parameter amount
    with pytest.raises(TypeError):
        crud.add_habit("name")
    
    # check error for wrong periodicity type
    assert crud.add_habit("name", "wrong") == -1

    # check error for wrong periodicity type
    assert crud.add_habit("name", PeriodicityTypes.DAY, note=True) == -2

    # check error for wrong periodicity type
    assert crud.add_habit("name", PeriodicityTypes.DAY, date=True) == -3

    # check error for wrong periodicity type
    assert crud.add_habit("name", PeriodicityTypes.DAY, active="") == -4

    # create one run 
    habit = crud.add_habit("habit 1", PeriodicityTypes.DAY)

    # check id for the first entry
    assert habit.id == 1
    
    # check if the correct periodicity was set
    assert habit.periodicity == PeriodicityTypes.DAY
    
    # check if the note is empty
    assert habit.note == None
    
    # check that it is auto set to active
    assert habit.active == True

    # fail a duplicate name
    assert crud.add_habit("habit 1", PeriodicityTypes.DAY) == -5

def test_delete_habit():
    crud = Crud()

    # create one for deletion 
    habit = crud.add_habit("habit 2 for delete", PeriodicityTypes.DAY)

    # check parameter amount
    with pytest.raises(TypeError):
        crud.delete_habit()

    # check if error if hand over id does not exists
    assert crud.delete_habit(-1) == -1

    # check delete
    assert crud.delete_habit(habit.id) == 1

def test_get_habit():
    crud = Crud()

    # check parameter amount
    with pytest.raises(TypeError):
        crud.get_habit()

    # check to get an not existing habit
    assert crud.get_habit(-1) == -1

    # check to get a real one
    habit = crud.get_habit(1)
    assert type(habit) is Habit

    # check if we get the requested one
    assert habit.id == 1


def test_activate_habit():
    crud = Crud()

    # check parameter amount
    with pytest.raises(TypeError):
        crud.activate_habit()

    # check parameter amount
    with pytest.raises(TypeError):
        crud.activate_habit("")

    # check ne state was not a bool
    assert crud.activate_habit(1, "") == -2

    # check habit was not found
    assert crud.activate_habit(-1, True) == -1
    
    # check update
    assert crud.activate_habit(1, False) == 1

    # check the habit
    habit = crud.get_habit(1)

    assert habit.active == False

def test_update_habit():
    crud = Crud()

    # check parameter amount
    with pytest.raises(TypeError):
        crud.activate_habit()

    # check an empty submit, without a change
    assert crud.update_habit(1) == -2

    # check not existing habit submit
    assert crud.update_habit(-1, name="any") == -1

    # check not existing habit submit
    assert crud.update_habit(-1, name="any") == -1

    # create one for duplicate name check 
    habit = crud.add_habit("habit 2", PeriodicityTypes.DAY)
    assert crud.update_habit(1, name="habit 2") == -3

    # check edit success
    assert crud.update_habit(1, name="habit 1 updated", note="note") == 1

    # check the habit
    habit_edited = crud.get_habit(1)

    assert habit_edited.name == "habit 1 updated"
    assert habit_edited.note == "note"
