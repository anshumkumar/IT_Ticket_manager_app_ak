from database.db import get_db_connection

class Ticket:
    def __init__(self, id, user_id, title, description, status, category, priority, staff_notes=None, additional_info=None):
        self.id = id
        self.user_id = user_id
        self.title = title
        self.description = description
        self.status = status
        self.category = category
        self.priority = priority
        self.staff_notes = staff_notes
        self.additional_info = additional_info

# this is the ticket class, it has attrubutes for tickets, explained in my class diagram and documentation.
# adding new functionality for staff to add notes to tickets, so im adding annother attribute called staff_notes.
# additional info functionality being added.

    def create_ticket(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO tickets (user_id, title, description, status, category, priority, device_id) VALUES (?, ?, ?, ?, ?, ?)',
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
            tickets.append(Ticket(
                row['id'],
                row['user_id'],
                row['title'],
                row['description'],
                row['status'],
                row['category'],
                row['priority'],
                row['staff_notes'],
                row['additional_info']
            ))
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
            tickets.append(Ticket(
                row['id'],
                row['user_id'],
                row['title'],
                row['description'],
                row['status'],
                row['category'],
                row['priority'],
                row['staff_notes'],
                row['additional_info']
            ))
        return tickets

    @staticmethod
    def get_all_tickets():
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute('''
        SELECT tickets.*, users.name, users.username
        FROM tickets
        JOIN users ON tickets.user_id = users.id
        ORDER BY priority DESC, id DESC  
        ''')
        # the last line sorts tickets by priority, it is one of the requirement for the app.

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
                row['priority'],
                row['staff_notes'],
                row['additional_info']
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

    # adding functionality to cancel a ticket.

    @staticmethod
    def cancel_ticket(ticket_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE tickets SET status = ? WHERE id = ?", ("Cancelled", ticket_id))
        conn.commit()
        conn.close()

    @staticmethod
    def staff_notes_update(ticket_id, notes):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE tickets SET staff_notes = ? WHERE id = ?", (notes, ticket_id))
        conn.commit()
        conn.close()

    @staticmethod
    def add_additional_info(ticket_id, additional_info):
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT additional_info FROM tickets WHERE id = ?", (ticket_id,))
        row = cursor.fetchone()

        existing_info = row["additional_info"] if row and row["additional_info"] else ""

        if existing_info:
            updated_info = existing_info + "\n\n--- New Update ---\n" + additional_info
        else:
            updated_info = additional_info

        cursor.execute(
        "UPDATE tickets SET additional_info = ?, status = ? WHERE id = ?",
        (updated_info, "Info Provided", ticket_id)
    )
        conn.commit()
        conn.close()

    #right now the user submits additional info but previous additional info dissapears, it needs to be fixed.
