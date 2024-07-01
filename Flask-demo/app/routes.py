from flask import render_template, url_for, redirect, request, flash
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from app import app, db, login_manager
from app.models import User

init_users = [
    {
        'username': 'admin',
        'password': 'admin',
        'email': 'admin@login.com',
        'role': 'admin',
        'description': 'Admin user'
    },
    {
        'username': 'Alice',
        'password': 'alice',
        'email': 'alice@login.com',
        'role': 'user',
        'description': 'Alice is a user'
    },
    {
        'username': 'Bob',
        'password': 'bob',
        'email': 'bob@login.com',
        'role': 'user',
        'description': 'Bob is a user'
    }
]


@app.cli.command('init')
def init():
    db.create_all()
    for user in init_users:
        new_user = User(
            username=user['username'],
            password=generate_password_hash(user['password']),
            email=user['email'],
            role=user['role'],
            description=user['description']
        )
        db.session.add(new_user)
    db.session.commit()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


def admin_required(f):
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        if current_user.role != 'admin':
            flash('You are not an admin!')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function


def currentuser_required(f):
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        if current_user.id != int(request.args.get('id')):
            flash('You are not the current user!')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        user = User.query.filter_by(username=username).first()
        if user:
            flash('Username already exists')
        else:
            new_user = User(
                username=username,
                password=generate_password_hash(password),
                email=email,
                role='user',
                description='New user'
            )
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login'))
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('profile'))
        else:
            flash('Invalid username or password')
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/admin')
@admin_required
def admin():
    users = User.query.all()
    return render_template('admin.html', users=users)


@app.route('/profile')
@login_required
def profile():
    user = User.query.get(current_user.id)
    return render_template('profile.html', user=user)


@app.route('/view')
@currentuser_required
def view():
    user_id = request.args.get('id')
    if user_id:
        user = User.query.get(user_id)
        return render_template('profile.html', user=user)
    flash('Please provide a user id')
    return redirect(url_for('index'))


@app.route('/edit', methods=['GET', 'POST'])
@currentuser_required
def edit():
    if request.method == 'POST':
        user_id = request.args.get('id')
        user = User.query.get(user_id)
        user.username = request.form['username']
        if request.form['password']:
            user.password = generate_password_hash(request.form['password'])
        user.email = request.form['email']
        user.role = request.form['role']
        user.description = request.form['description']
        db.session.commit()
        return redirect(url_for('profile'))
    user_id = request.args.get('id')
    user = User.query.get(user_id)
    return render_template('edit.html', user=user)
