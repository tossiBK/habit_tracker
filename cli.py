import fire
from crud import Crud
from tracking import Tracking
from analytics import Analytics


class Internal_Habit():
    """
    group class for receiving and formatting the input and return the status messags to the conosle.
    used for all CRUD actions
    """
    def add(self, name, periodicity, note = None, date = None, active = None):
        # check input

        crud = Crud()

        result = crud.add_habit(name, periodicity, note, date, active)

        return result
    
    def delete(self, habit_id):
        crud = Crud()
        result = crud.delete_habit(habit_id)

        return result
    
    def pause(self, habit_id):
        crud = Crud()
        result = crud.activate_habit(habit_id, False)

        return result
    
    def unpause(self, habit_id):
        crud = Crud()
        result = crud.activate_habit(habit_id, True)

        return result
    
    def update(self, habit_id, name=None, note=None):
        # check at least one need to be entered

        crud = Crud()
        result = crud.update_habit(habit_id, name, note)

        return result
    
    def show(self, habit_id):
        crud = Crud()
        result = crud.get_habit(habit_id)

        output = f"name:\t{result.name}\n" \
            f"note:\t{result.note}\n" \
            f"periodicity:\t{result.periodicity}\n" \
            f"created:\t{result.created}\n" \
            f"active:\t{result.active}\n"
            
        
        return output


class Internal_Tracking():
    """
    group class for receiving and formatting the input and return the status messags to the conosle.
    used for all tracking actions
    """
    def add(self, habit_id, date=None):
        tracking = Tracking()
        result = tracking.add(habit_id)

        return result
    


class Internal_Analytics():
    """
    group class for receiving and formatting the input and return the status messags to the conosle.
    used for all analytics actions
    """
    def show_all(self, active=True):
        analytics = Analytics()

        data = analytics.show_all_habits(active)

        output = f"Id\tName\n"
        for habit in data:
            output += f"{habit.id}\t{habit.name}\n"

        return output
    
    def show_by_periodicity(self, periodicity):
        # check input

        analytics = Analytics()

        data = analytics.show_all_habits_by_periodicity(periodicity)

        output = f"Id\tName\n"
        for habit in data:
            output += f"{habit.id}\t{habit.name}\n"

        return output
    
    def show_streaks(self, habit_id=None):
        analytics = Analytics()

        data = analytics.show_longest_streak(habit_id)

        output = f"Id\tName - longest streak\n"
        for habit in data:
            output += f"{habit.id}\t{habit.name} - streak: {habit.streak}\n"

        return output


class Cli():
    """
    Main class for Cli, which take care of the registering of the groups inside.

    """
    def __init__(self):
        self.tracking = Internal_Tracking()
        self.habit = Internal_Habit()
        self.analytics = Internal_Analytics()
    
    


if __name__ == '__main__':
    fire.Fire(Cli)