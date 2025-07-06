import sqlite3
import os
import hashlib
import uuid
from flask import g

DATABASE_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
                             'database.db')


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE_PATH)
        db.row_factory = sqlite3.Row
    return db


def init_db():
    """Initialize the database with the users table if it doesn't exist."""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    # Create users table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id TEXT PRIMARY KEY,
        username TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    conn.commit()
    conn.close()


def hash_password(password, salt=None):
    """Hash a password with SHA-256 and a random salt."""
    if salt is None:
        salt = uuid.uuid4().hex

    hashed = hashlib.sha256((password + salt).encode()).hexdigest()
    return f"{salt}${hashed}"


def check_password(stored_password, provided_password):
    """Verify a stored password against a provided password."""
    salt, hashed = stored_password.split('$')
    return hashed == hashlib.sha256((provided_password + salt).encode()).hexdigest()


class User:
    @staticmethod
    def create(username, email, password):
        """Create a new user in the database."""
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()

        user_id = str(uuid.uuid4())
        hashed_password = hash_password(password)

        try:
            cursor.execute(
                "INSERT INTO users (id, username, email, password) VALUES (?, ?, ?, ?)",
                (user_id, username, email, hashed_password)
            )
            conn.commit()
            return User.get_by_id(user_id)
        except sqlite3.IntegrityError:
            # Username or email already exists
            return None
        finally:
            conn.close()

    @staticmethod
    def get_by_id(user_id):
        """Get a user by their ID."""
        conn = sqlite3.connect(DATABASE_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        user = cursor.fetchone()
        conn.close()

        return dict(user) if user else None

    @staticmethod
    def get_by_email(email):
        """Get a user by their email."""
        conn = sqlite3.connect(DATABASE_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        user = cursor.fetchone()
        conn.close()

        return dict(user) if user else None

    @staticmethod
    def get_by_username(username):
        """Get a user by their username."""
        conn = sqlite3.connect(DATABASE_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        conn.close()

        return dict(user) if user else None

    @staticmethod
    def authenticate(email, password):
        """Authenticate a user by email and password."""
        user = User.get_by_email(email)

        if user and check_password(user['password'], password):
            return user

        return None

