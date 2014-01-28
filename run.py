"""Simple Flask Application

Usage:
  run.py createdb
  run.py createdb --testdata
  run.py server
  run.py server <host>:<port>

Options:
  -h --help     Show this screen.

"""
import os
import glob
import random
import importlib

import picka
from docopt import docopt

from app.controllers.home import app
from app.models.author import Author
from app.models.book import Book
from app.models.user import User
from settings import BaseModel, engine, db_session, DEBUG, SECRET_KEY


HOST = 'localhost:5000'


def get_modulename(path_to_file):
    return path_to_file.split('/')[-1].split('.')[0]

def createdb():
    print(' --- Create Tables --- ')
    print(" Start create tables ... ")

    all_models = glob.glob(os.path.join(os.path.dirname(__file__),
                                        'app', 'models', '*.py'))

    for model in all_models:
        modulepath = 'app.models.{modulename}'.format(
                        modulename=get_modulename(model))

        importlib.import_module(modulepath)

    BaseModel.metadata.create_all(bind=engine)
    print("All tables was create")

def fake_user():
    print('Make fake user (test/test)')

    user = User(login='test', password='test', is_active=True,
                name="Bob Smith")
    db_session.add(user)
    db_session.commit()

def fake_books_and_authors():
    print('Create fake books and authors')

    for _ in xrange(5):
        book = Book(name=picka.sentence_actual(min_words=1, max_words=4))
        db_session.add(book)

        for _ in xrange(random.randrange(1, 4)):
            author = Author(name=picka.name())
            db_session.add(author)

            book.authors.append(author)

    db_session.commit()

def fake_data():
    print(' --- Fake Data --- ')

    fake_user()
    fake_books_and_authors()

    print(' --- Fake Data Created Success --- ')

def run_server(host=None):
    if host is None:
        host = HOST

    host, port = host.split(':')

    all_views = glob.glob(os.path.join(os.path.dirname(__file__),
                                        'app', 'controllers', '*.py'))

    for view in all_views:
        modulepath = 'app.controllers.{modulename}'.format(
                modulename=get_modulename(view))
        viewmodule = importlib.import_module(modulepath)

        blueprint = getattr(viewmodule, 'bp', None)

        if blueprint is not None:
            url_prefix = '/{url}'.format(url=blueprint.name)
            app.register_blueprint(blueprint, url_prefix=url_prefix)

    app.secret_key = SECRET_KEY
    app.run(debug=DEBUG, host=host, port=int(port))


if __name__ == '__main__':
    arguments = docopt(__doc__)
    
    if arguments.get('createdb', None):
        createdb()

        if arguments.get('--testdata', None):
            fake_data()

    if arguments.get('server', None):
        run_server(host=arguments.get('<host>:<port>', None))
