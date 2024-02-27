from db import (
    get_habit_by_periodicity,
    get_longest_streak,
    get_streak_for_habit,
)

class Analytics:
    def __init__(self, db, habit_id, user_id, periodicity):
        self.db = db
        self.habit_id = habit_id
        self.user_id = user_id
        self.periodicity = periodicity

    def get_habit_by_periodicity(self):
        return get_habit_by_periodicity(self.db, self.user_id, self.periodicity)
    
    def get_longest_streak(self):
        return get_longest_streak(self.db, self.user_id)
    
    def get_streak_for_habit(self):
        return get_streak_for_habit(self.db, self.habit_id)

    def __str__(self):
        return f'Analytics for habit {self.habit_id}'