from optparse import check_choice
import re
from flask import Flask, render_template, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, ValidationError
from wtforms.validators import DataRequired, EqualTo, Length
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date
from werkzeug.security import generate_password_hash, check_password_hash

#  Create a Flask Instance
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretversion'
# Add Database Connection
# Old SQLite DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///codemy.db'
#  New MySQL DB
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost/name'

db = SQLAlchemy(app)

@app.route('/date/')
def date_for_json():
    favorite_games = {
        "Jora": "Futbol",
        "Kerwen": "Woleybol",
        "Mergen": "Judo"
    }
    return favorite_games
    # return {"Date": date.today() }

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(150), nullable=False, unique=True)
    favorite_color = db.Column(db.String(120))
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    password_hash = db.Column(db.String(120))

    @property
    def password(self):
        raise AttributeError('password is not a readable')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<Name %r>' % self.name

# db.drop_all()
# db.create_all()

class UserForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    favorite_color = StringField('Favorite Color')
    password_hash = PasswordField('Password', validators=[DataRequired(), EqualTo('password_hash2', message='Password Must Match')])
    password_hash2 = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Submit')

class PasswordForm(FlaskForm):
    email = StringField('What is Your Email', validators=[DataRequired()])
    password = PasswordField('What is Your Password', validators=[DataRequired()])
    submit = SubmitField('Submit')


@app.route('/update/<int:id>/', methods=['GET', 'POST'])
def update(id):
    form = UserForm()
    update_db_user = Users.query.get_or_404(id)
    if request.method == 'POST':
        update_db_user.name = request.form['name']
        update_db_user.email = request.form['email']
        update_db_user.favorite_color = request.form['favorite_color']
        try:
            db.session.commit()
            flash("User update succsesfull")
            return render_template("update_to_username.html", form=form, update_db_user=update_db_user)

        except Exception as ex:
            flash("Error!")
            return render_template("update_to_username.html", form=form, update_db_user=update_db_user)

    else:
        return render_template("update_to_username.html", form=form, update_db_user=update_db_user, id=id)

@app.route('/delete/<int:id>/')
def delete(id):
    user_to_delete = Users.query.get_or_404(id)
    name = None
    form = UserForm()
    try:
        db.session.delete(user_to_delete)
        db.session.commit()
        flash('User deleted successfully')
        our_users = Users.query.order_by(Users.date_added)         
        return render_template("add_user.html", name=name, form=form, our_users=our_users)

    except Exception as ex:
        flash('Error deleting user')


# Create  a Form Class
class NamerForm(FlaskForm):
    name = StringField('What is your name', validators=[DataRequired()])
    submit = SubmitField('Submit')

# BooleanField, DateField, DateTimeField, DecimalField, FileField, HiddenField, MultipleField, FieldList,
# FloatField, FormField, IntegerField, PasswordField, RadioField, SelectField, SubmitField, StringField, TextAreaField

# Validators
# DataRequired, Email, EqualTo, InputRequired, IPAddress, Length, MacAddress, NumberRagnge, 
# Optional, Regexp, URL, UUID, AnyOf, NoneOf


# Create a routes decorator
# @app.route('/')
# def index():
#     return '<h1>Hello world</h1>'

# safe, capitalize, lower, upper, title, trim, striptags

@app.route('/user/add/', methods=['GET', 'POST'])
def add_user():
    name = None
    form = UserForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None:
            hashed_pw = generate_password_hash(form.password_hash.data, 'sha256')
            user = Users(name=form.name.data, email=form.email.data, favorite_color=form.favorite_color.data, password_hash=hashed_pw)
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        form.name.data = ''
        form.email.data = ''
        form.favorite_color.data = ''
        form.password_hash.data = ''
        flash('User adedd Successfuly') 
    our_users = Users.query.order_by(Users.date_added)         
    return render_template("add_user.html", name=name, form=form, our_users=our_users)
    

# Call to html file
@app.route('/')
def index():
    first_name = 'Kerwen'
    # second_name = '<strong>Abdullayew</strong>'
    second_name = 'Abdullayew'
    flash("Welcome To Our Website!")
    favorite_pissa = ['Corekli doner', 'Lawashly doner', 'palow usti', 'Iskender']
    return render_template("index.html", 
                            first_name=first_name,
                            second_name=second_name,
                            favorite_pissa=favorite_pissa
                            )


# localhost:5000/user/jora/26
@app.route('/user/<string:name>/<int:age>/')
def user(name, age):
    return render_template("user.html", user_name = name, user_age = age)

# Create Custom Error Pages
# Invalid URL
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

# Internal Server Error
@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html"), 500

@app.route('/test_pw/', methods=['GET', 'POST'])
def test_pw():
    email = None
    password = None
    pw_to_check = None
    passed = None
    form = PasswordForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        form.email.data = ''
        form.password.data = ''
        pw_to_check = Users.query.filter_by(email=email).first()
        passed = check_password_hash(pw_to_check.password_hash, password)

    return render_template("test_pw.html",
                            email=email,
                            password=password, 
                            pw_to_check = pw_to_check,
                            passed =passed,
                            form=form)

@app.route('/name/', methods=['GET', 'POST'])
def name():
    name = None
    form = NamerForm()
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
        flash("Form submited succsesfull")
    return render_template("name.html",
                            name=name, 
                            form=form)

if __name__ == '__main__':
    app.run(debug=True)