__author__ = 'alex'

from wtforms import Form, IntegerField, validators

class NewGameForm(Form):
    rows = IntegerField('Number of Rows:', [validators.NumberRange(min=5, max=50), validators.DataRequired()])
    columns = IntegerField('Number of Columns', [validators.NumberRange(min=5, max=50), validators.DataRequired()])
    mines = IntegerField('Number of Mines', [validators.NumberRange(min=5, max=99), validators.DataRequired()])