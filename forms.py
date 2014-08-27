__author__ = 'alex'

from flask.ext.wtf import Form
from wtforms import IntegerField, validators


class NewGameForm(Form):
    rows = IntegerField('rows', [validators.NumberRange(min=5, max=50), validators.DataRequired()])
    columns = IntegerField('columns', [validators.NumberRange(min=5, max=50), validators.DataRequired()])
    mines = IntegerField('mines', [validators.NumberRange(min=5, max=99), validators.DataRequired()])