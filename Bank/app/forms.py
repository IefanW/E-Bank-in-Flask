from flask_wtf import FlaskForm
from wtforms import StringField,FloatField
from wtforms.validators import DataRequired

#Stipulate the form of database
class UserForm(FlaskForm):
    name = StringField('name',validators=[DataRequired()])
    pwd = StringField('pwd',validators=[DataRequired()])
    email = StringField('email',validators=[DataRequired()])

class AccountForm(FlaskForm):
    save = FloatField('save',validators=[DataRequired()])
    withdraw = FloatField('withdraw',validators=[DataRequired()])