from database import Database
from model.Habit import Habit, PeriodicityTypes
from datetime import datetime

class Crud():
    """
    Class provides all functions for the CRUD operations.

    Methods
    -------
    add_habit(self, name, periodicity, note = None, date = None, active = None)
        adds a new habit. 
    delete_habit(self, habit_id)
        deletes a given habit
    activate_habit(self, habit_id, status)
        set the status of a habit to active or inactive.
    update_habit(self, habit_id, name=None, note=None)
        allows to update  a certain habits name and note.
    get_habit(self, habit_id)
        returns the details of a habit
    """
    
    def add_habit(self, name, periodicity, note = None, date = None, active = None):
        """
        adds a new habit.

        Parameters
        ----------
        name : str
           name for the new habit
        periodicity : str
           sets the interval in which the habit is planed to be performed. allwoed values: 'd' (daily), 'w' (weekly), 'm' (monthly)

        Returns
        -------
        habit : Habit or int
            returns the habit or a failure code in case of an error
            -1: periodicity was not from the type PeriodicityTypes
            -2: note was not a string
            -3: date was not from type datetime
            -4: active was not a bool
            -5: habit name is already in use
        """
        # check values
        if type(periodicity) is not PeriodicityTypes:
            return -1
        
        if note is not None and type(note) is not str:
            return -2
        
        if date is not None and type(date) is not datetime:
           return -3
            
        if active is not None and type(active) is not bool:
           return -4
        
        db = Database()
        
        habit = Habit()
        habit.name = name
        habit.periodicity = periodicity

        # add optional fields if set
        if date is not None:
            habit.created = date
        
        if note is not None:
            habit.note = note

        if active is not None:
            habit.active = active
       
        
        result = db.add_habit(habit)

        # forward and map error for unique constraint
        if result == -1:
            return -5

        return habit

    def delete_habit(self, habit_id):
        """
        deletes the provided habit

        Parameters
        ----------
        habit_id : int
            id of the habit to delete

        Returns
        -------
        status_code : int
            code if the habit was added succesful, or a failure code in case of an error
             1: success
            -1: habit was not found
        """
        db = Database()

        # get habit 
        # check the id and test if the habit exists
        habit = db.get_habit(habit_id)

        if habit is None:
            return -1
        
        result = db.delete_habit(habit)
        return 1

    def activate_habit(self, habit_id, status):
        """
        change the state for active / inactive for the provided habit

        Parameters
        ----------
        habit_id : int
            id of the habit to delete
        status : bool
            state to be set for the habit True (active), False (inactive)

        Returns
        -------
        status_code : int
            code if the habit was added succesful, or a failure code in case of an error
             1: success
            -1: habit was not found
            -2: dtate was not a bool
        """
        # check input
        if status is not None and type(status) is not bool:
           return -2
        
        db = Database()

        # get habit 
        # check the id and test if the habit exists
        habit = db.get_habit(habit_id)

        if habit is None:
            return -1
        
        habit.active = status
        status = db.commit()

        return 1

    def update_habit(self, habit_id, name=None, note=None):
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

        Returns
        -------
        status_code : int
            code if the habit was added succesful, or a failure code in case of an error
             1: success
            -1: habit was not found
            -2: no values added to change, at least one must be submitted
            -3: habit name is already in use
        """
        # check input
        if note is None and name is None:
            return -2

        db = Database()
        # get habit 
        # check the id and test if the habit exists
        habit = db.get_habit(habit_id)

        if habit is None:
            return -1
        
        if name is not None:
            habit.name = name

        if note is not None:
            habit.note = note

        result = db.commit()

        # forward and map error for unique constraint
        if result == -1:
            return -3

        return 1

    def get_habit(self, habit_id):
        """
        returns a habit for the provided habit id.

        Parameters
        ----------
        habit_id : int
            id of the habit to receive

        Returns
        -------
        habit : Habit or int
            Returns the habit if exists for the habit_id, otherwise an error code
            -1: habit was not found
        """
        db = Database()

        # get habit 
        # check the id and test if the habit exists
        habit = db.get_habit(habit_id)

        if habit is None:
            return -1
        
        return habit