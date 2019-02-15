from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import Form, StringField, TextAreaField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models import User

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])

    submit = SubmitField('Sign Up')
# checking if username already exits in db
    def validate_username(self, username):
        # filtering by first username entered
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken, please choose a different one')

    # checking if email already exits in db
    def validate_email(self, email):
        # filtering by first email entered
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken, please choose a different one')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    
    submit = SubmitField('Sign In')

class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators = [FileAllowed(['jpg', 'png'])])   # permitting desired image file formats

    submit = SubmitField('Update')

# checking if username already exits in db
    def validate_username(self, username):
        if username.data != current_user.username:
            # filtering by first username entered(validation checks)
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken, please choose a different one')

    # checking if email already exits in db
    def validate_email(self, email):
        if email.data != current_user.email:
            # filtering by first email entered
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken, please choose a different one')
# creating post
class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')

