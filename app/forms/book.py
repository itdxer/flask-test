from flask.ext.wtf import Form
from wtforms import TextField, SelectMultipleField, widgets
from wtforms.validators import Required

from app.models.author import Author


class BookForm(Form):
    name = TextField('name', validators = [Required()])
    authors = SelectMultipleField('Authors',
        choices=[(author.id, author.name) for author in Author.query.all()],
        widget = widgets.ListWidget(prefix_label=False),
        option_widget = widgets.CheckboxInput()
    )
