from flask.ext.wtf import Form
from wtforms import TextField
from wtforms.validators import Required


class AuthorForm(Form):
    name = TextField('name', validators = [Required()])
