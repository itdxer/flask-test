from flask import (Blueprint, render_template, request, redirect, url_for,
                   abort)
from sqlalchemy import desc

from app.helper.auth import auth_requierd
from app.forms.author import AuthorForm
from app.models.author import Author
from settings import db_session


bp = Blueprint("author", __name__, template_folder="../../templates/author")


@bp.route('/', methods=('GET',))
@auth_requierd
def all_authors():
    authors = db_session.query(Author).order_by(desc(Author.id))
    return render_template('author_all.html', page='author', authors=authors)

@bp.route('/delete/<int:author_id>/', methods=('GET',))
@auth_requierd
def delete_author(author_id):
    db_session.query(Author).filter(Author.id == author_id).delete()
    return redirect(url_for('author.all_authors'))

@bp.route('/update/<int:author_id>/', methods=('GET', 'POST'))
@auth_requierd
def update_author(author_id):
    author = db_session.query(Author).filter(Author.id == author_id).first()

    if not author:
        abort(404)

    form = AuthorForm(obj=author)

    if request.method == 'POST' and form.validate_on_submit():
        form.populate_obj(author)
        db_session.add(author)
        db_session.commit()

        return redirect(url_for('author.all_authors'))

    return render_template('author_form.html', page='author', form=form)

@bp.route('/create/', methods=('GET', 'POST'))
@auth_requierd
def create_author():
    form = AuthorForm()

    if request.method == 'POST' and form.validate_on_submit():
        author = Author()
        form.populate_obj(author)
        db_session.add(author)
        db_session.commit()

        return redirect(url_for('author.all_authors'))

    return render_template('author_form.html', page='author', form=form)
