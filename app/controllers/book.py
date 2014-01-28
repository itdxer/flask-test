from flask import (Blueprint, render_template, redirect, url_for, request,
                   abort)
from sqlalchemy import desc

from app.helper.auth import auth_requierd
from app.forms.book import BookForm
from app.models.author import Author
from app.models.book import Book
from settings import db_session


bp = Blueprint("book", __name__, template_folder="../../templates/book")


@bp.route('/', methods=('GET',))
@auth_requierd
def all_books():
    books = db_session.query(Book).order_by(desc(Book.id))
    return render_template('book_all.html', page='book', books=books)

@bp.route('/delete/<int:book_id>/', methods=('GET',))
@auth_requierd
def delete_book(book_id):
    db_session.query(Book).filter(Book.id == book_id).delete()
    return redirect(url_for('book.all_books'))

@bp.route('/update/<int:book_id>/', methods=('GET', 'POST'))
@auth_requierd
def update_book(book_id):
    book = db_session.query(Book).filter(Book.id == book_id).first()

    if not book:
        abort(404)

    form = BookForm(obj=book)
    form.authors.data = [str(author.id) for author in book.authors]

    if request.method == 'POST' and form.name.data:
        old_authors = book.authors
        new_authors = db_session.query(Author).filter(
                        Author.id.in_(request.form.getlist('authors'))).all()

        removed_authors = set(old_authors) - set(new_authors)
        for author in removed_authors:
            book.authors.remove(author)

        added_authors = set(new_authors) - set(old_authors)
        for author in added_authors:
            book.authors.append(author)

        db_session.add(book)
        db_session.commit()

        return redirect(url_for('book.all_books'))

    return render_template('book_form.html', page='book', form=form)

@bp.route('/create/', methods=('GET', 'POST'))
@auth_requierd
def create_book():
    form = BookForm()

    if request.method == 'POST' and form.name.data:
        book = Book(name=form.name.data)

        book.authors = db_session.query(Author).filter(
                        Author.id.in_(request.form.getlist('authors'))).all()

        db_session.add(book)
        db_session.commit()

        return redirect(url_for('book.all_books'))

    return render_template('book_form.html', page='book', form=form)
