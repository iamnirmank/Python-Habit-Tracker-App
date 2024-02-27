import os
import pytest
from db import (
    create_habit,
    create_tables,
    create_user,
    get_db,
    check,
    get_all_tracked_habits,
    get_habit_by_periodicity,
    get_longest_streak,
    get_streak_for_habit,
    login_user,
)

class TestDB:

    def setup_method(self):
        self.db = get_db('mock_db')
        create_tables(self.db)
        self.db.commit()
        create_user(self.db, 'nirmankhadka.student@gmail.com', 'test_password')
        user = login_user(self.db, 'nirmankhadka.student@gmail.com', 'test_password')
        self.user_id = user[0]
        create_habit(self.db, 'test_task', 'test_periodicity', self.user_id)
        habit = get_habit_by_periodicity(self.db, self.user_id, 'test_periodicity')
        self.habit_id = habit[0]

    def test_check(self): 
        assert check(self.db, self.habit_id) == True

    def test_get_all_tracked_habits(self): 
        assert get_all_tracked_habits(self.db, self.user_id) == [(1, 'test_task', 'test_periodicity', 1, '[]')]

    def test_get_habit_by_periodicity(self):
        assert get_habit_by_periodicity(self.db, self.user_id, 'test_periodicity') == (1, 'test_task', 'test_periodicity', 1, '[]')

    def test_get_longest_streak(self):
        assert get_longest_streak(self.db, self.habit_id) == 0

    def test_get_streak_for_habit(self):
        check(self.db, self.habit_id)
        assert get_streak_for_habit(self.db, self.habit_id) == 1

    def teardown_method(self):
        self.db.close()
        os.remove('mock_db')

pytest.main(['-v', 'test_project.py'])
