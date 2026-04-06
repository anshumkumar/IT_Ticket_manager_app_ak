from database.db import get_db_connection

class Ticket:
    def __init__(self, id, user_id, title, description, status, category, priority):
        self.id = id
        self.user_id = user_id
        self.title = title
        self.description = description
        self.status = status
        self.category = category
        self.priority = priority

    def create_ticket(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO tickets (user_id, title, description, status, category, priority) VALUES (?, ?, ?, ?, ?, ?)',
                       (self.user_id, self.title, self.description, self.status, self.category, self.priority))
        conn.commit()
        conn.close()

    @staticmethod
    def get_user_tickets(user_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM tickets WHERE user_id = ?', (user_id,))
        rows = cursor.fetchall()
        conn.close()
        tickets = []
        for row in rows:
            tickets.append(Ticket(row['id'], row['user_id'], row['title'], row['description'], row['status'], row['category'], row['priority']))
        return tickets
    
    @staticmethod
    def get_all_tickets():
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM tickets')
        rows = cursor.fetchall()
        conn.close()
        tickets = []
        for row in rows:
            tickets.append(Ticket(row['id'], row['user_id'], row['title'], row['description'], row['status'], row['category'], row['priority']))
        return tickets
    
    @staticmethod
    def update_ticket_status(ticket_id, status):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('UPDATE tickets SET status = ? WHERE id = ?', (status, ticket_id))
        conn.commit()
        conn.close()