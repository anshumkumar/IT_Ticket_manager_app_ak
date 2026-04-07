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
# this is the ticket class, it has attrubutes for tickets, explained in my class diagram and documentation.


    def create_ticket(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO tickets (user_id, title, description, status, category, priority) VALUES (?, ?, ?, ?, ?, ?)',
                       (self.user_id, self.title, self.description, self.status, self.category, self.priority))
        conn.commit()
        conn.close()
    # creates a tickets and saves details to the database.

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
    # gets tickets for a particular user by using their user id.

    @staticmethod
    def get_tickets_by_user(user_id):
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

        cursor.execute('''
        SELECT tickets.*, users.name, users.username
        FROM tickets
        JOIN users ON tickets.user_id = users.id
        ''')

        rows = cursor.fetchall()
        conn.close()

        tickets = []
        for row in rows:
            ticket = Ticket(
                row['id'],
                row['user_id'],
                row['title'],
                row['description'],
                row['status'],
                row['category'],
                row['priority']
            )

            ticket.user_name = row['name']
            ticket.username = row['username']

            tickets.append(ticket)

        return tickets
    # staff must be able to review all tickets.
    # multiple staff will be working. In a real app ratio of users will be more than staff.
    # so therefore one staff member could be working on multiple user queries.
    # by sorting tickets by users they can keep track of it.

    @staticmethod
    def update_ticket_status(ticket_id, status):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('UPDATE tickets SET status = ? WHERE id = ?', (status, ticket_id))
        conn.commit()
        conn.close()

    # for staff to update status of a ticket.