from flask import session, Blueprint, render_template, request, redirect, url_for, flash, make_response
from .models import db, User, Auth
from werkzeug.security import generate_password_hash

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return make_response("hello")
    # users = User.query.all()
    new_user = User(full_name="<NAME>")
    db.session.add(new_user)
    db.session.commit()

    db.session(User).all()
    db.session(User).filter(User.id==1).all()
    # return render_template('index.html', users=users)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        full_name = request.form['full_name']
        email = request.form['email']
        mobile = request.form.get('mobile')
        username = request.form['username']
        password = request.form['password']
        user_type = request.form['user_type']

        existing_user = User.query.filter_by(email=email).first()
        existing_auth = Auth.query.filter_by(username=username).first()

        if existing_user or existing_auth:
            flash('Email or username already registered. Please log in.', 'error')
            return redirect(url_for('main.register'))

        try:
            new_user = User(full_name=full_name, email=email, mobile=mobile)
            db.session.add(new_user)
            db.session.flush()

            new_auth = Auth(username=username, password=password, user_type=user_type, user_id=new_user.id)
            db.session.add(new_auth)

            db.session.commit()

            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('main.login'))

        except Exception as e:
            db.session.rollback()
            flash('An error occurred while registering. Please try again.', 'error')
            print(f"Error: {e}")
            return redirect(url_for('main.register'))

    return render_template('register.html')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user_auth = Auth.query.filter_by(username=username, password=password).first()
        if user_auth:
            session['user_id'] = user_auth.user_id  # Store user ID in session
            flash(f'Welcome, {user_auth.user.full_name}!', 'success')
            return redirect(url_for('main.home'))
        else:
            flash('Invalid username or password', 'error')
            return redirect(url_for('main.login'))

    return render_template('login.html')

@bp.route('/admin_dashboard')
def admin_dashboard():
    user_id = session.get('user_id')
    if not user_id:
        flash('Please log in first', 'error')
        return redirect(url_for('main.login'))
    
    user = User.query.get(user_id)
    if user.auth.user_type != 'Admin':
        flash('Access denied.', 'error')
        return redirect(url_for('main.home'))

    return render_template('admin_dashboard.html', user=user)

@bp.route('/user_dashboard')
def user_dashboard():
    user_id = session.get('user_id')
    if not user_id:
        flash('Please log in first', 'error')
        return redirect(url_for('main.login'))
    
    user = User.query.get(user_id)
    return render_template('user_dashboard.html', user=user)

@bp.route('/home')
def home():
    user_id = session.get('user_id')
    if not user_id:
        flash('Please log in first', 'error')
        return redirect(url_for('main.login'))

    user = User.query.filter_by(id=user_id).first()
    if not user:
        flash('User not found', 'error')
        return redirect(url_for('main.login'))

    return render_template('home.html', user=user)

@bp.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.login'))

@bp.route('/users')
def users_service():
    return make_response("hellow users")