from flask import Blueprint, render_template, request, redirect, url_for, flash, session, g
from app.models.user import User, init_db
import functools

auth = Blueprint('auth', __name__)


# Initialize the database when the app starts
@auth.before_app_request
def before_request():
    init_db()
    user_id = session.get('user_id')
    if user_id:
        g.user = User.get_by_id(user_id)
    else:
        g.user = None


def login_required(view):
    """Decorator to require login for views."""

    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)

    return wrapped_view


@auth.route('/signup', methods=('GET', 'POST'))
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        error = None

        if not username:
            error = 'Username is required.'
        elif not email:
            error = 'Email is required.'
        elif not password:
            error = 'Password is required.'
        elif password != confirm_password:
            error = 'Passwords do not match.'
        elif User.get_by_username(username):
            error = f"User {username} is already registered."
        elif User.get_by_email(email):
            error = f"Email {email} is already registered."

        if error is None:
            user = User.create(username, email, password)
            if user:
                # Log the user in after signup
                session.clear()
                session['user_id'] = user['id']
                return redirect(url_for('main.index'))
            else:
                error = "Error creating user. Please try again."

        flash(error)

    return render_template('auth/signup.html')


@auth.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        error = None
        user = User.get_by_email(email)

        if user is None:
            error = 'Incorrect email.'
        elif not User.authenticate(email, password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('main.index'))

        flash(error)

    return render_template('auth/login.html')


@auth.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main.index'))

