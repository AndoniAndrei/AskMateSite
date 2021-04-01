from functools import wraps

import bcrypt
from flask import session, redirect, url_for
from datetime import datetime


def date_and_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def hash_password(plain_text_password):
    # By using bcrypt, the salt is saved into the hash itself
    hashed_bytes = bcrypt.hashpw(plain_text_password.encode('utf-8'), bcrypt.gensalt())
    return hashed_bytes.decode('utf-8')





def login_required(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        if 'username' in session:
            return function(*args, **kwargs)
        else:
            return redirect(url_for('login'))
    return wrapper
