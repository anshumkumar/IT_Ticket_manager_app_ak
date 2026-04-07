import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))   
db_path = os.path.join(BASE_DIR, 'tickets.db')

def get_db_connection():
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

# I have defined a function to create sqlite tables.
# these are used to store user information and ticket details.
# staff and users are seperated through role attribute.

def create_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,  
                        username TEXT NOT NULL,
                        password TEXT NOT NULL,
                        role TEXT NOT NULL
                    )''')
                   
    cursor.execute('''CREATE TABLE IF NOT EXISTS tickets (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   user_id INTEGER NOT NULL,
                   title TEXT NOT NULL,
                   description TEXT NOT NULL,
                   status TEXT NOT NULL,
                   category TEXT NOT NULL,
                   priority INTEGER NOT NULL
                   )''')
    conn.commit()
    conn.close()