import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))   
db_path = os.path.join(BASE_DIR, 'tickets.db')

def get_db_connection():
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
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
                   
                   
    try:
        cursor.execute("ALTER TABLE tickets ADD COLUMN staff_notes TEXT")
    except sqlite3.OperationalError:
        pass

    cursor.execute('''CREATE TABLE IF NOT EXISTS devices (
                   device_id INTEGER PRIMARY KEY AUTOINCREMENT,
                   assigned_to INTEGER NOT NULL,
                   device_name TEXT NOT NULL,
                   device_type TEXT NOT NULL,
                   serial_number TEXT NOT NULL,
                   location TEXT NOT NULL,
                   last_maintenance_date TEXT NOT NULL,

                   FOREIGN KEY (assigned_to) REFERENCES users(id)    
                   )''')
                   
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_table()