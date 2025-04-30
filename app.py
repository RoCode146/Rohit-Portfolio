from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mail import Mail, Message
from datetime import datetime
import mysql.connector

app = Flask(__name__)
app.secret_key = 'b3fdc73681c24716aa9ae8d69c93cde6e02a347a21393e243c5f4cf122fa7e6e'

# ------------------ Database Connection ------------------
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1611",
    database="taskify"
)
cursor = mydb.cursor(dictionary=True)

# ------------------ Mail Configuration ------------------
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'rohitsutar1611@gmail.com'
app.config['MAIL_PASSWORD'] = 'taab uknu vqzb otxo'

mail = Mail(app)

# ------------------ Routes ------------------
@app.route('/')
def index():
    cursor.execute("SELECT * FROM services")
    services = cursor.fetchall()

    cursor.execute("SELECT * FROM projects")
    projects = cursor.fetchall()

    return render_template('index.html', services=services, projects=projects, now=datetime.now())

@app.route('/contact', methods=['POST'])
def contact():
    name = request.form['name']
    email = request.form['email']
    message = request.form['message']

    cursor.execute(
        "INSERT INTO contacts (name, email, message, status) VALUES (%s, %s, %s, %s)",
        (name, email, message, 'Pending')
    )
    mydb.commit()

    msg = Message(
        subject=f"New Contact from {name}",
        sender=email,
        recipients=['rohitsutar1611@gmail.com'],
        body=f"From: {name} <{email}>\n\n{message}"
    )
    mail.send(msg)
    flash("Your message has been sent successfully!", 'success')
    return redirect(url_for('index'))

# ------------------ Admin Authentication ------------------
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username == 'admin' and password == 'password':
            session['admin'] = True
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid credentials!', 'danger')
    return render_template('admin_login.html')

# ✅ Add admin logout route
@app.route('/admin/logout')
def admin_logout():
    session.pop('admin', None)
    flash('You have been logged out successfully!', 'info')
    return redirect(url_for('admin_login'))

# ------------------ Admin Dashboard ------------------
@app.route('/admin/dashboard')
def admin_dashboard():
    if 'admin' not in session:
        return redirect(url_for('admin_login'))

    cursor.execute("SELECT * FROM services")
    services = cursor.fetchall()

    cursor.execute("SELECT * FROM projects")
    projects = cursor.fetchall()

    cursor.execute("SELECT * FROM contacts")
    contacts = cursor.fetchall()

    return render_template('admin_dashboard.html', services=services, projects=projects, contacts=contacts)

# ------------------ Admin Services Management ------------------
@app.route('/admin/add_service', methods=['POST'])
def add_service():
    if 'admin' not in session:
        return redirect(url_for('admin_login'))

    title = request.form['title']
    description = request.form['description']

    cursor.execute("INSERT INTO services (title, description) VALUES (%s, %s)", (title, description))
    mydb.commit()

    flash('Service added successfully!', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/delete_service/<int:id>')
def delete_service(id):
    if 'admin' not in session:
        return redirect(url_for('admin_login'))

    cursor.execute("DELETE FROM services WHERE id = %s", (id,))
    mydb.commit()

    flash('Service deleted successfully!', 'info')
    return redirect(url_for('admin_dashboard'))

# ------------------ Admin Projects Management ------------------
@app.route('/admin/add_project', methods=['POST'])
def add_project():
    if 'admin' not in session:
        return redirect(url_for('admin_login'))

    title = request.form['title']
    description = request.form['description']
    link = request.form['link']  # Capture the project link from the form
    if not link:
            return "Error: Link is required", 400
    cursor.execute("INSERT INTO projects (title, description, link) VALUES (%s, %s, %s)", (title, description, link))
    mydb.commit()

    flash('Project added successfully!', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/delete_project/<int:id>')
def delete_project(id):
    if 'admin' not in session:
        return redirect(url_for('admin_login'))

    cursor.execute("DELETE FROM projects WHERE id = %s", (id,))
    mydb.commit()

    flash('Project deleted successfully!', 'info')
    return redirect(url_for('admin_dashboard'))

# ------------------ Admin Contacts Management ------------------
@app.route('/admin/add_contact_response', methods=['POST'])
def add_contact_response():
    if 'admin' not in session:
        return redirect(url_for('admin_login'))

    name = request.form['name']
    email = request.form['email']
    message = request.form['message']
    status = 'Pending'

    cursor.execute(
        "INSERT INTO contacts (name, email, message, status) VALUES (%s, %s, %s, %s)",
        (name, email, message, status)
    )
    mydb.commit()

    flash('Contact message added successfully!', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/delete_contact/<int:id>')
def delete_contact(id):
    if 'admin' not in session:
        return redirect(url_for('admin_login'))

    cursor.execute("DELETE FROM contacts WHERE id = %s", (id,))
    mydb.commit()

    flash('Contact message deleted successfully!', 'info')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/reply_contact/<int:id>', methods=['POST'])
def reply_contact(id):
    if 'admin' not in session:
        return redirect(url_for('admin_login'))

    cursor.execute("SELECT * FROM contacts WHERE id = %s", (id,))
    contact = cursor.fetchone()

    if not contact:
        flash('Contact not found!', 'danger')
        return redirect(url_for('admin_dashboard'))

    reply_message = request.form['reply_message']

    html_body = f"""
    <html>
    <body>
        <h2>Reply to Your Message</h2>
        <p>Dear {contact['name']},</p>
        <p><b>Your Message:</b><br>{contact['message']}</p>
        <p><b>Our Response:</b><br>{reply_message}</p>
        <p>Best regards,<br>Taskify Team</p>
    </body>
    </html>
    """

    msg = Message(
        subject="Reply to Your Message - Taskify",
        sender=app.config['MAIL_USERNAME'],
        recipients=[contact['email']],
        body=f"Dear {contact['name']},\n\nThank you for your message: \"{contact['message']}\"\n\nOur response:\n{reply_message}\n\nBest regards,\nTaskify Team",
        html=html_body
    )
    mail.send(msg)

    cursor.execute("UPDATE contacts SET status = 'Resolved' WHERE id = %s", (id,))
    mydb.commit()

    flash('Reply sent successfully!', 'success')
    return redirect(url_for('admin_dashboard'))

# ------------------ Main App Run ------------------
if __name__ == '__main__':
    app.run(debug=True)
