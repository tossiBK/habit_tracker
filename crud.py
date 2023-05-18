from database import Database
from model.Habit import Habit, PeriodicityTypes

class Crud():
    
    def add_habit(self, name, periodicity, note = None, date = None, active = None):
        db = Database()
        
        # todo check data
        habit = Habit()
        habit.name = name
        
        match periodicity:
            case "d":
                habit.periodicity = PeriodicityTypes.DAY
            case "w":
                habit.periodicity = PeriodicityTypes.WEEK
            case "m":
                habit.periodicity = PeriodicityTypes.MONTH
            case __:
                #throw error
                return -1
        
        db.add_habit(habit)

        return 1

    def delete_habit(self, habit_id):
        db = Database()

        # get habit 
        # check the id and test if the habit exists
        habit = db.get_habit(habit_id)

        if habit is None:
            return "Error, not found"
        
        db.delete_habit(habit)
        return {'code': 1, 'msg': "success"}

    def activate_habit(self, habit_id, status):
        db = Database()

        # check input

        # get habit 
        # check the id and test if the habit exists
        habit = db.get_habit(habit_id)

        if habit is None:
            return "Error, not found"
        
        habit.active = status
        db.commit()

        return {'code': 1, 'msg': "success"}

    def update_habit(self, habit_id, name=None, note=None):
        db = Database()

        # check input

        # get habit 
        # check the id and test if the habit exists
        habit = db.get_habit(habit_id)

        if habit is None:
            return "Error, not found"
        
        if name is not None:
            habit.name = name

        if note is not None:
            habit.note = note

        result = db.commit()

        if result['code'] != 1:
            return result

        return {'code': 1, 'msg': "success"}

    def get_habit(self, habit_id):
        db = Database()

        # check input

        # get habit 
        # check the id and test if the habit exists
        habit = db.get_habit(habit_id)

        if habit is None:
            return "Error, not found"
        
        return habit