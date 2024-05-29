from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL

class RegisterForm(FlaskForm):
    email = StringField("Email")
    name = StringField("Name")
    password = StringField("Password")
