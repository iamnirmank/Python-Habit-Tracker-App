import os
from db import get_db
from user import User
from habit import Habit
from analyse import Analytics
import random
from datetime import datetime, timedelta

def create_habit(db, user_id):
    try:
        print("-----------------------------") 
        task = input('Enter the task: ')
        periodicity = input('Enter the periodicity: ')
        habit = Habit(db, None, task, periodicity, user_id)
        habit.create()
        print('Habit created successfully!')
        print("-----------------------------") 
    except Exception as e:
        print('Error creating habit:', e)
        print("-----------------------------") 

def check_habit(db, user_id):
    try:
        habit = Habit(db, None, None, None, user_id)
        habits = habit.get_all_tracked_habits()
        print("-----------------------------") 
        print('Tracked habits:')
        for habit in habits:
            print(habit)
        print("-----------------------------")
        habit_id = input('Enter the habit ID to check: ')
        habit = Habit(db, habit_id, None, None, user_id)
        habit.check()
        print("-----------------------------")
        print('Habit checked successfully!')
        print("-----------------------------") 
    except Exception as e:
        print('Error checking habit:', e)
        print("-----------------------------") 

def login_user(db):
    try:
        print("-----------------------------") 
        email = input('Enter your email: ')
        password = input('Enter your password: ')
        print("-----------------------------")
        print
        user = User(db, email, password)
        user = user.login()
        create_predefined_habits(db, user[0])
        if user:
            print('Login successful!')
            return user
            print("-----------------------------") 
        else:
            print("-----------------------------") 
            print('Login failed!')
            return None
    except Exception as e:
        print("-----------------------------") 
        print('Error logging in:', e)
        return None

def register_user(db):
    try:
        print("-----------------------------") 
        email = input('Enter your email: ')
        password = input('Enter your password: ')
        print("-----------------------------")
        user = User(db, email, password)
        user.register()
        print('User registered successfully!')
        print("-----------------------------") 
    except Exception as e:
        print("-----------------------------") 
        print('Error registering user:', e)

def create_predefined_habits(db, user_id):
    try:
        predefined_habits = [
            ("Exercise", "daily", generate_continuous_check_dates()),
            ("Read a book", "daily", generate_continuous_check_dates()),
            ("Weekly review", "weekly", generate_weekly_continuous_check_dates()),
            ("Meditation", "daily", generate_continuous_check_dates()),
            ("Learn something new", "daily", generate_continuous_check_dates()),
        ]

        for task, periodicity, check_dates in predefined_habits:
            habit = Habit(db, None, task, periodicity, user_id, check_dates)
            habit.create()

    except Exception as e:
        print('Error creating predefined habits:', e)
def generate_continuous_check_dates():
    start_date = datetime.now() - timedelta(days=30)
    check_dates = [(start_date + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(30)]
    return check_dates

def generate_random_check_dates():
    num_dates = random.randint(5, 15)
    start_date = datetime.now() - timedelta(days=365)
    end_date = datetime.now()
    check_dates = [(start_date + timedelta(days=random.randint(0, 365))).strftime('%Y-%m-%d') for _ in range(num_dates)]
    return check_dates

def generate_weekly_continuous_check_dates():
    start_date = datetime.now() - timedelta(days=365)
    check_dates = [(start_date + timedelta(weeks=i)).strftime('%Y-%m-%d') for i in range(52)]
    return check_dates

def analytics(db, user_id):
    try:
        analytics = Analytics(db, None, user_id, None)
        habits = Habit(db, None, None, None, user_id)
        all_habits = habits.get_all_tracked_habits()
        
        print('Tracked habits:')
        for habit in all_habits:
            print(habit)

        while True:
            print("-----------------------------") 
            print('1. Longest streak for all habits')
            print('2. Longest Streak for a habit')
            print('3. Get habit by periodicity')
            print('4. Quit')
            print("-----------------------------") 
            choice = input('Enter your choice: ')

            if choice == '1':
                print('Longest streak:', analytics.get_longest_streak())
            elif choice == '2':
                habit_id = input('Enter the habit ID before to proceed further: ')
                analytics.habit_id = habit_id
                print('Streak:', analytics.get_streak_for_habit())
            elif choice == '3':
                periodicity = input('Enter the periodicity: ')
                analytics.periodicity = periodicity
                print('Habit:', analytics.get_habit_by_periodicity())
            elif choice == '4':
                break
            else:
                print('Invalid choice. Please try again.')
        print("-----------------------------") 
    except Exception as e:
        print('Error getting analytics:', e)

def CLI():
    db = get_db('habit_tracker.db')
    user = User(db, None, None)
    user.create_tables()
    while True:
        print("-----------------------------") 
        print('Welcome to Habit Tracker!')
        print("-----------------------------") 
        print('1. Register')
        print('2. Login')
        print('3. Quit')
        print("-----------------------------") 
        choice = input('Enter your choice: ')
        if choice == '1':
            register_user(db)
        elif choice == '2':
            user = login_user(db)
            user_id = user[0]
            if user_id:
                while True:
                    print("-----------------------------") 
                    print('1. Create a habit')
                    print('2. Check a habit')
                    print('3. View analytics')
                    print('4. Quit')
                    print("-----------------------------") 
                    choice = input('Enter your choice: ')
                    if choice == '1':
                        create_habit(db, user_id)
                    elif choice == '2':
                        check_habit(db, user_id)
                    elif choice == '3':
                        analytics(db, user_id)
                    elif choice == '4':
                        print('Goodbye!')
                        db.close()
                        os.remove('habit_tracker.db')
                        break
        else:
            print('Goodbye!')
            break

if __name__ == '__main__':
    CLI()
