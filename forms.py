from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import InputRequired

class AddUserForm(FlaskForm):
    """ Form for User """

    username = StringField("Username", validators=[InputRequired()])
    password = StringField("Password", validators=[InputRequired()])
    email = StringField("Email Address", validators=[InputRequired()])
    first_name = StringField("First Name", validators=[InputRequired()])
    last_name = StringField("Last Name", validators=[InputRequired()])

class LoginUserForm(FlaskForm):
    """ Form for Loging In """

    username = StringField("Username", validators=[InputRequired()])
    password = StringField("Password", validators=[InputRequired()])

class AddFeedbackForm(FlaskForm):
    """ Form for Feedback """

    title = StringField("Title", validators=[InputRequired()])
    content = StringField("Content", validators=[InputRequired()])

class UpdateFeedbackForm(FlaskForm):
    """ Form for updating the Feedback """

    title = StringField("Title", validators=[InputRequired()])
    content = StringField("Content", validators=[InputRequired()])