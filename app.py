from flask import Flask, render_template, request, redirect, url_for, session
from models.tickets import Ticket
from database.db import create_table
from models.user import User

app = Flask(__name__)
app.secret_key = 'anshum_key'

create_table()

# This is the login route for app.
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.get_user(username)
# checks if user exists, the credentials added by user match or not.
        if user and user.password == password:
            session['user_id'] = user.id
            session['username'] = user.username
            session['role'] = user.role    
# if the role is staff, it takes you to staff dashboard
            if user.role == 'staff':
                return redirect(url_for('staff_dashboard'))
            else:
                return redirect(url_for('user_dashboard'))
# admin dashboard has been removed for simplicity.
        return render_template('login.html', error='You have entered an invalid username or password. Please try again.')
# this is the error message above, for wrong credentials.
    return render_template('login.html')
# if credentials are correct, it takes user to user dashboard and staff to the staff one.

# this route is for registering a user, also checks if user already exists by comparing name and username.
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        username = request.form['username']
        password = request.form['password']

        user_exists = User.get_user(username)
        if user_exists:
            return render_template('register.html', error='This account already exists.')
# this is displayed if user already exists.

        new_user = User(None, name, username, password, 'user')
        new_user.create_user()
        # this creates new user, adds them to database.
        # create user function is defined in user.py file. 

        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))
# for logging out, it clears the session and takes user to login page.


@app.route('/user_dashboard')
def user_dashboard():
    if 'user_id' not in session or session.get('role') != 'user':
        return redirect(url_for('login'))

    user_id = session['user_id']
    tickets = Ticket.get_user_tickets(user_id)
    return render_template('user_dashboard.html', tickets=tickets)
# user dashboard, fetches tickets of the particular user.


@app.route('/staff_dashboard')
def staff_dashboard():
    if 'user_id' not in session or session.get('role') != 'staff':
        return redirect(url_for('login'))

    tickets = Ticket.get_all_tickets()
    return render_template('staff_dashboard.html', tickets=tickets)

# staff dashboard, fetches all of the tickets created by a;; users.


@app.route('/submit_ticket', methods=['GET', 'POST'])
def submit_ticket():
    if 'user_id' not in session or session.get('role') != 'user':
        return redirect(url_for('login'))

    if request.method == 'POST':
        user_id = session['user_id']
        title = request.form['title']
        description = request.form['description']
        category = request.form['category']
        priority = int(request.form['priority'])
        status = 'Open'

        new_ticket = Ticket(None, user_id, title, description, status, category, priority)
        new_ticket.create_ticket()
# adds ticket to database.
# create_ticket function is defined in tickets.py file, it adds the ticket to database.
        return redirect(url_for('user_dashboard'))

    return render_template('submit_ticket.html')


@app.route('/ticket/<int:ticket_id>/complete', methods=['POST'])
def complete_ticket(ticket_id):
    if 'user_id' not in session or session.get('role') != 'staff':
        return redirect(url_for('login'))

    Ticket.update_ticket_status(ticket_id, 'Closed')
    return redirect(url_for('staff_dashboard'))
# when staff reviews the ticket, they can change its status as completed.


if __name__ == '__main__':
    app.run(debug=True)