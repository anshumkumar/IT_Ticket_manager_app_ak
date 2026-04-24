from flask import Flask, render_template, request, redirect, url_for, session
from models.tickets import Ticket
from database.db import create_table 
from database.db import get_db_connection
from models.user import User
from models.devices import Device
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.secret_key = 'anshum_key'

create_table()

# This is the login route for app.
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()

        if not username or not password:
            return render_template('login.html', error='Username and password are required.')

        user = User.get_user(username)
# new update: adding password hashing here:
        if user: 
            password_stored = user.password
            password_right = False   #this statement is declared at beginning
            if password_stored.startswith("pbkdf2:") or password_stored.startswith("scrypt:"):
                password_right = check_password_hash(password_stored, password)
                # this will ensure new passwords are hashed
            else:
                password_right = (password_stored == password)
                # this is for old accounts created without the use of hash.
                # old accounts cant be deleted because they have data used for testing.

            if password_right:
                session['user_id'] = user.id
                session['username'] = user.username
                session['role'] = user.role    
            # new update, adding admin functionality.
                if user.role == 'admin':
                    return redirect(url_for('admin_dashboard'))
# if the role is staff, it takes you to staff dashboard
                elif user.role == 'staff':
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
        name = request.form.get('name', '').strip()
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()

        if not name or not username or not password:
            return render_template('register.html', error='All fields are required.')

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


@app.route("/user_dashboard")
def user_dashboard():
    if 'user_id' not in session or session.get('role') != 'user':
        return redirect(url_for('login'))

    tickets = Ticket.get_tickets_by_user(session["user_id"])
    devices = Device.get_all_devices()

    return render_template(
        "user_dashboard.html",
        tickets=tickets,
        devices=devices,
        reply=None
    )
# user dashboard, fetches tickets of the particular user.


@app.route('/staff_dashboard')
def staff_dashboard():
    if 'user_id' not in session or session.get('role') != 'staff':
        return redirect(url_for('login'))

    tickets = Ticket.get_all_tickets()
    devices = Device.get_all_devices()
    return render_template('staff_dashboard.html', tickets=tickets, devices=devices)

# staff dashboard, fetches all of the tickets created by a;; users.


@app.route('/submit_ticket', methods=['GET', 'POST'])
def submit_ticket():
    if 'user_id' not in session or session.get('role') != 'user':
        return redirect(url_for('login'))

    if request.method == 'POST':
        user_id = session['user_id']
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        category = request.form.get('category', '').strip()
        priority = request.form.get('priority', '').strip()
        status = 'Open'

        

        new_ticket = Ticket(None, user_id, title, description, status, category, int(priority))
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

# devices management route.

@app.route('/devices')
def view_devices():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    devices = Device.get_all_devices()
    return render_template('devices.html', devices=devices)

# adding a device.

@app.route("/add_device", methods=["GET", "POST"])
def add_device():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    if request.method == "POST":
        device_name = request.form.get("device_name", "").strip()
        device_type = request.form.get("device_type", "").strip()
        assigned_to = request.form.get("assigned_to", "").strip()
        serial_number = request.form.get("serial_number", "").strip()
        location = request.form.get("location", "").strip()
        last_maintenance_date = request.form.get("last_maintenance_date", "").strip()

        if not device_name or not device_type or not assigned_to or not serial_number or not location or not last_maintenance_date:
            users = User.get_all_users()
            return render_template("add_device.html", users=users, error="All fields are required.")

        device = Device(
            None,
            device_name,
            device_type,
            int(assigned_to),
            serial_number,
            location,
            last_maintenance_date
        )
        device.add_device()

        if session.get('role') == 'staff':    
            return redirect(url_for('staff_dashboard'))
        else:
            return redirect(url_for('user_dashboard'))
        # this is fixed, so now application users will be redirected to their dashboard.

    users = User.get_all_users()
    return render_template("add_device.html", users=users)

@app.route("/delete_device/<int:device_id>", methods=["POST"])
def delete_device(device_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    Device.delete_device(device_id)
    return redirect(url_for("view_devices"))

# in tickets.py cancel_ticket function has been created.
# so here i am adding the app route for it.

@app.route('/ticket/<int:ticket_id>/cancel', methods=['POST'])
def cancel_ticket(ticket_id):
    if 'user_id' not in session or session.get('role') != 'user':
        return redirect(url_for('login'))

    Ticket.cancel_ticket(ticket_id)
    return redirect(url_for('user_dashboard'))


@app.route('/ticket/<int:ticket_id>/notes', methods=['POST'])
def update_staff_notes(ticket_id):
    if 'user_id' not in session or session.get('role') != 'staff':
        return redirect(url_for('login'))

    notes = request.form.get('staff_notes', '')
    Ticket.staff_notes_update(ticket_id, notes)
    return redirect(url_for('staff_dashboard'))

# staff requesting for more info

@app.route('/ticket/<int:ticket_id>/info_needed', methods=['POST'])
def info_for_ticket(ticket_id):
    if 'user_id' not in session or session.get('role') != 'staff':
        return redirect(url_for('login'))

    Ticket.update_ticket_status(ticket_id, 'Awaiting Info')
    return redirect(url_for('staff_dashboard'))

@app.route('/ticket/<int:ticket_id>/additional_info', methods=['POST'])
def info_provided(ticket_id):
    if 'user_id' not in session or session.get('role') != 'user':
        return redirect(url_for('login'))

    additional_info = request.form.get('additional_info', '').strip()

    if not additional_info:
        return redirect(url_for('user_dashboard'))

    Ticket.add_additional_info(ticket_id, additional_info)
    return redirect(url_for('user_dashboard'))


# adding admin app route

@app.route('/admin_dashboard')
def admin_dashboard():
    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect(url_for('login'))

    users = User.get_all_users()


    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE password_request = 1")
    requests = cursor.fetchall()
    conn.close()

    return render_template('admin_dashboard.html', users=users, requests = requests)


# functionality for admin to delete user accounts.
@app.route('/admin/delete_account/<int:user_id>', methods=['POST'])
def delete_account_admin(user_id):
    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect(url_for('login'))

    if user_id == session['user_id']:
        return redirect(url_for('admin_dashboard'))

    User.delete_user(user_id)
    return redirect(url_for('admin_dashboard'))

# functionality for admin to change a users password. 

@app.route('/admin/reset_password_admin/<int:user_id>', methods=['POST'])
def reset_password_admin(user_id):
    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect(url_for('login'))

    new_pass = request.form.get('new_pass', '').strip()

    if not new_pass:
        return redirect(url_for('admin_dashboard'))

    User.password_change(user_id, new_pass)
    return redirect(url_for('admin_dashboard'))

# users and staff can request password reset.

@app.route('/req_pass_reset', methods=['POST'])
def req_pass_reset():
    if 'user_id' not in session  or session.get('role') != 'user':
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE users SET password_request = 1 WHERE id = ?",
        (session['user_id'],)
    )
    conn.commit()
    conn.close()

    return redirect(url_for('user_dashboard'))

# adding functionality for a chatbot
# python dictionries will be used for this simple chatbot.

@app.route('/app_chatbot', methods=['POST'])
def app_chatbot():
    if 'user_id' not in session or session.get('role') != 'user':
        return redirect(url_for('login'))

    msg = request.form.get('message', '').lower().strip()

    faq_answers = {
        "password": "To change your password, click 'Request Password Change'.",
        "submit ticket": "Click 'Submit a New Ticket'.",
        "cancel ticket": "You can cancel tickets from your dashboard.",
        "device": "Use 'Add Device' from the sidebar.",
        "status": "Check ticket status in your dashboard."
    }

    reply = "Sorry, I am unable to help you, please contact the admin."

    for key in faq_answers:
        if key in msg:
            reply = faq_answers[key]
            break

    tickets = Ticket.get_tickets_by_user(session["user_id"])
    devices = Device.get_all_devices()

    return render_template(
        "user_dashboard.html",
        tickets=tickets,
        devices=devices,
        reply=reply
    )



if __name__ == '__main__':
    app.run(debug=True)

# repository test.

#testing if changes are saved on github.
#test
#test test