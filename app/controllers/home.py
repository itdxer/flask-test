from flask import Flask, render_template, redirect, session, request, url_for

from app.models.author import Author
from app.models.book import Book, authors
from app.models.user import User
from settings import db_session


app = Flask(__name__, template_folder='../../templates')


@app.route('/', methods=("GET",))
def home():
    return render_template("home.html", page="home")

@app.route('/search/', methods=('GET',))
def search_book():
    book_name = request.args.get('book')
    author_name = request.args.get('author')

    books = db_session.query(Book).outerjoin(authors, Author)\
                      .filter(Book.name == book_name)\
                      .filter(Author.name == author_name)

    return render_template("search.html", books=books, page="home")

@app.route('/login/', methods=("POST",))
def login():
    if request.method == 'POST':
        login = request.form['login']
        password = request.form['password']
        user = db_session.query(User).filter(User.login == login,
                                             User.is_active == True).first()

        if user and user.check_password(password):
            session['auth_user_id'] = user.id

    return redirect(request.referrer)

@app.route('/logout/', methods=("GET",))
def logout():
    session.pop('auth_user_id', None)
    return redirect(url_for('home'))
