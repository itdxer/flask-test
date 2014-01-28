import hashlib

from flask import session
from sqlalchemy import Column, Integer, String, Boolean

from settings import BaseModel, db_session


class User(BaseModel):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100))
    login = Column(String(50))
    password = Column(String(225))
    is_active = Column(Boolean, default=False)

    @staticmethod
    def hash_password(password):
        return hashlib.sha224(password).hexdigest()

    @classmethod
    def current(cls):
        if 'auth_user_id' in session:
            return db_session.query(cls)\
                             .filter(cls.id == session['auth_user_id'])

    def check_password(self, password):
        return self.password == User.hash_password(password)

    def __init__(self, *args, **kwargs):
        kwargs['password'] = User.hash_password(kwargs['password'])
        super(User, self).__init__(*args, **kwargs)
