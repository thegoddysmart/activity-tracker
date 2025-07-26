from flask import Flask, render_template, redirect, url_for, request, session, flash
from repository import *
from werkzeug.security import check_password_hash, generate_password_hash
from models import Status
import os
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

# Use environment variable for secret key in production
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-key")

db = TaskManagerDB("sqlite:///activities.db", True)

@app.route('/')
def index():
    return redirect(url_for('dashboard') if 'user_id' in session else 'login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = db.find_user_by_email(email)

        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            return redirect(url_for('dashboard'))
        flash('Invalid email or password', 'error')
        return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        if db.user_exists(email):
            flash('This email is already linked to an account', 'error')
        else:
            hashed_password = generate_password_hash(password)
            db.add_user(name, email, hashed_password)
            flash('Account created successfully!', 'success')
            return redirect(url_for('login'))

    return render_template('signup.html')

@app.route('/dashboard', methods=['GET'])
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user = db.get_user(session['user_id'])
    tasks = db.find_tasks_by_user_id(user.id)
    return render_template('dashboard.html', user=user, tasks=tasks)

@app.route('/tasks/<int:task_id>', methods=['GET', 'POST'])
def view_task(task_id):
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        status = request.form['status']
        db.update_task(task_id, title, description, status)
        return redirect(url_for('dashboard'))

    task = db.get_task(task_id)
    return render_template('task_details.html', task=task, Status=Status)

@app.route('/change-status/<int:task_id>', methods=['POST'])
def update_status(task_id):
    status = request.form['status']
    task = db.get_task(task_id)
    db.update_task(task_id, task.title, task.description, status)
    return render_template('task_details.html', task=task, Status=Status)

@app.route('/add_task', methods=['POST'])
def add_task():
    if 'user_id' in session:
        title = request.form['title']
        description = request.form['description']
        db.add_task(title, description, session['user_id'])
    return redirect(url_for('dashboard'))

@app.route('/delete-task/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    db.remove_task(task_id)
    flash(f"Task {task_id} deleted successfully", "success")
    return redirect(url_for('dashboard'))

@app.route('/delete-account', methods=['POST'])
def delete_user():
    if 'user_id' in session:
        db.remove_user(session['user_id'])
        session.pop('user_id')
    return redirect(url_for('signup'))

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
