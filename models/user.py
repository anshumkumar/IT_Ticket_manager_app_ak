from database.db import get_db_connection

class User:
    def __init__(self, id, name, username, password, role):
        self.id = id
        self.name = name
        self.username = username
        self.password = password
        self.role = role

    def create_user(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (name, username, password, role) VALUES (?, ?, ?, ?)',
                       (self.name, self.username, self.password, self.role))
        conn.commit()
        conn.close()
    
    @staticmethod
    def get_user(username):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return User(row['id'], row['name'], row['username'], row['password'], row['role'])
        return None
    
    # gets all users, this is developed because its required for devices page.
    @staticmethod
    def get_all_users():
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users')
        rows = cursor.fetchall()
        conn.close()

        users = []
        for row in rows:
            users.append(User(
                row['id'],
                row['name'],
                row['username'],
                row['password'],
                row['role']
            ))
        return users



