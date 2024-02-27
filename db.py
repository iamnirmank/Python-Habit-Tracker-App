from datetime import datetime, timedelta
import json
import sqlite3

def get_db(name='main.db'):
    """
    Returns a connection to the database.

    Args:
        name (str): The name of the SQLite database file.

    Returns:
        sqlite3.Connection: A connection to the SQLite database.
    """
    return sqlite3.connect(name)

def create_tables(database):
    """
    Creates necessary tables if they do not exist in the database.

    Args:
        database (sqlite3.Connection): The SQLite database connection.
    """
    with database:
        cur = database.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS user (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT,
            password TEXT
        )''')

        cur.execute('''CREATE TABLE IF NOT EXISTS habit (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT,
            periodicity TEXT,
            user_id INTEGER,
            check_dates TEXT DEFAULT '[]',
            FOREIGN KEY (user_id) REFERENCES user(id)
        )''')

def create_user(database, email, password):
    """
    Creates a new user in the database.

    Args:
        database (sqlite3.Connection): The SQLite database connection.
        email (str): The email of the user.
        password (str): The password of the user.
    """
    with database:
        cur = database.cursor()
        cur.execute('INSERT INTO user (email, password) VALUES (?, ?)', (email, password))

def login_user(db, email, password):
    """
    Logs in the user.

    Args:
        db (sqlite3.Connection): The SQLite database connection.
        email (str): The email of the user.
        password (str): The password of the user.

    Returns:
        tuple: The user information if login is successful, otherwise None.
    """
    cur = db.cursor()
    cur.execute('SELECT * FROM user WHERE email = ? AND password = ?', (email, password))
    user = cur.fetchone()
    return user if user else None

def create_habit(db, task, periodicity, user_id, check_dates):
    """
    Creates a new habit in the database.

    Args:
        db (sqlite3.Connection): The SQLite database connection.
        task (str): The task associated with the habit.
        periodicity (str): The periodicity of the habit.
        user_id (int): The ID of the user.
        check_dates (list): The dates the habit was checked.
    """
    periodicity = periodicity.lower()
    cur = db.cursor()
    cur.execute('INSERT INTO habit (task, periodicity, user_id, check_dates) VALUES (?, ?, ?, ?)', (task, periodicity, user_id, json.dumps(check_dates)))
    db.commit()

def update_habit(db, habit_id, task, periodicity):
    """
    Updates an existing habit in the database.

    Args:
        db (sqlite3.Connection): The SQLite database connection.
        habit_id (int): The ID of the habit to update.
        task (str): The updated task associated with the habit.
        periodicity (str): The updated periodicity of the habit.
    """
    cur = db.cursor()
    cur.execute('UPDATE habit SET task = ?, periodicity = ? WHERE id = ?', (task, periodicity, habit_id))
    db.commit()
    
def delete_habit(db, habit_id):
    """
    Deletes a habit from the database.

    Args:
        db (sqlite3.Connection): The SQLite database connection.
        habit_id (int): The ID of the habit to delete.
    """
    cur = db.cursor()
    cur.execute('DELETE FROM habit WHERE id = ?', (habit_id,))
    db.commit()

def get_habit(db, habit_id):
    """
    Retrieves habit details by ID.

    Args:
        db (sqlite3.Connection): The SQLite database connection.
        habit_id (int): The ID of the habit to retrieve.

    Returns:
        tuple: The habit details if found, otherwise None.
    """
    cur = db.cursor()
    cur.execute('SELECT * FROM habit WHERE id = ?', (habit_id,))
    return cur.fetchone()

def check(db, habit_id, date):
    """
    Checks the habit as completed for the day.
    """
    cur = db.cursor()
    cur.execute('SELECT check_dates FROM habit WHERE id = ?', (habit_id,))
    result = cur.fetchone()
    if result:
        dates_json_str = result[0]  
        dates = json.loads(dates_json_str)
        if date:
            dates.append(date)
        else:
            dates.append(str(datetime.date.today()))
        cur.execute('UPDATE habit SET check_dates = ? WHERE id = ?', (json.dumps(dates), habit_id))
        db.commit()
        return True
    else:
        return False  
    
def get_all_tracked_habits(db, user_id):
    """
    Retrieves all habits tracked by the user.

    Args:
        db (sqlite3.Connection): The SQLite database connection.
        user_id (int): The ID of the user.

    Returns:
        list: A list of habits tracked by the user.
    """
    cur = db.cursor()
    cur.execute('SELECT * FROM habit WHERE user_id = ?', (user_id,))
    return cur.fetchall()

def get_habit_by_periodicity(db, user_id, periodicity):
    """
    Retrieves a habit by its periodicity.

    Args:
        db (sqlite3.Connection): The SQLite database connection.
        user_id (int): The ID of the user.
        periodicity (str): The periodicity of the habit.

    Returns:
        tuple: The habit if found, otherwise None.
    """
    periodicity = periodicity.lower()
    cur = db.cursor()
    cur.execute('SELECT * FROM habit WHERE user_id = ? AND periodicity = ?', (user_id, periodicity))
    return cur.fetchall()

def get_longest_streak(db, user_id):
    """
    Return the longest run streak of all defined habits.

    Args:
        db (sqlite3.Connection): The SQLite database connection.
        user_id (int): The ID of the user.

    Returns:
        int: The longest run streak of all defined habits.
    """
    cur = db.cursor()
    cur.execute('SELECT id FROM habit WHERE user_id = ?', (user_id,))
    habit_ids = [habit[0] for habit in cur.fetchall()]
    longest_streak = 0
    for habit_id in habit_ids:
        streak = get_streak_for_habit(db, habit_id)
        if streak > longest_streak:
            longest_streak = streak
    return longest_streak


def get_streak_for_habit(db, habit_id):
    """
    Return the longest run streak for a given habit.

    Args:
        db (sqlite3.Connection): The SQLite database connection.
        habit_id (int): The ID of the habit.

    Returns:
        int: The longest run streak for a given habit.
    """
    cursor = db.cursor()
    cursor.execute('SELECT check_dates FROM habit WHERE id = ?', (habit_id,))
    habit_dates = cursor.fetchone()[0]
    cursor.close()
    habit_dates = eval(habit_dates)
    streak = 0
    current_streak = 0
    today = datetime.now().date()
    yesterday = today - timedelta(days=1)

    for date_str in reversed(habit_dates):
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
        if date == yesterday:
            current_streak += 1
            yesterday = date
        elif date == today:
            current_streak += 1
            today = yesterday
            yesterday = date
        else:
            break

    streak = current_streak if current_streak > streak else streak
    return streak
