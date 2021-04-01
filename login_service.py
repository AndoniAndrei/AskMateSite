import bcrypt
from flask import session

import repositories


def verify_password(plain_text_password, hashed_password):
    hashed_bytes_password = hashed_password.encode('utf-8')
    return bcrypt.checkpw(plain_text_password.encode('utf-8'), hashed_bytes_password)


def login(username, plain_text_password):

    if repositories.username_exist(username):
        hashed_password = repositories.get_hashed_password(username)

        if verify_password(plain_text_password, hashed_password):
            session['username'] = username
            return

    raise EnvironmentError('Invalid Username and/or Password!')
