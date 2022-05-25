from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, ValidationError
from wtforms.validators import DataRequired, EqualTo, Length
from wtforms.widgets import TextArea
# from flask_ckeditor import CKEditorField
# BooleanField, DateField, DateTimeField, DecimalField, FileField, HiddenField, MultipleField, FieldList,
# FloatField, FormField, IntegerField, PasswordField, RadioField, SelectField, SubmitField, StringField, TextAreaField

# Validators
# DataRequired, Email, EqualTo, InputRequired, IPAddress, Length, MacAddress, NumberRagnge, 
# Optional, Regexp, URL, UUID, AnyOf, NoneOf

class SearchForm(FlaskForm):
    searched = StringField('Search', validators=[DataRequired()])
    submit = SubmitField('Submit')
    
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Submit')

class UserForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    favorite_color = StringField('Favorite Color')
    password_hash = PasswordField('Password', validators=[DataRequired(), EqualTo('password_hash2', message='Password Must Match')])
    password_hash2 = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Submit')

class PasswordForm(FlaskForm):
    email = StringField('What is Your Email', validators=[DataRequired()])
    password = PasswordField('What is Your Password', validators=[DataRequired()])
    submit = SubmitField('Submit')

# Create  a Form Class
class NamerForm(FlaskForm):
    name = StringField('What is your name', validators=[DataRequired()])
    submit = SubmitField('Submit')

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    slug = StringField('Slug', validators=[DataRequired()])
    content = StringField('Content', validators=[DataRequired()], widget=TextArea())
    # content = CKEditorField('Content', validators=[DataRequired()])
    submit= SubmitField('Submit')