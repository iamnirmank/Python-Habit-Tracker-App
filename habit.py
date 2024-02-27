from db import (
    create_habit,
    check,
    get_all_tracked_habits,
)
class Habit:
    def __init__(self, db, id, task, periodicity, user_id, check_dates=None):
        self.db = db
        self.task = task
        self.periodicity = periodicity
        self.user_id = user_id
        self.id = id
        self.check_dates = check_dates

    def create(self):
        create_habit(self.db, self.task, self.periodicity, self.user_id, self.check_dates)

    def check(self):
        check(self.db, self.id, date=None)

    def get_all_tracked_habits(self):
        return get_all_tracked_habits(self.db, self.user_id)



