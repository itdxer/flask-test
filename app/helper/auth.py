from functools import wraps

from flask import session, abort


def auth_requierd(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        if 'auth_user_id' not in session:
            abort(404)
        return f(*args, **kwargs)
    return wrapped
