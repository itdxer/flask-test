# -*- coding: utf-8 -*-
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

DEBUG = True

DATABASE = "sqlite:///database.db"
SECRET_KEY = '3jS9wfKvMBaMF2F5CResjMx97BPJZQc9gxnjSmI9zk4wBuGzUU8jrNo4Bar'

engine = create_engine(DATABASE, convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
BaseModel = declarative_base()
BaseModel.query = db_session.query_property()
