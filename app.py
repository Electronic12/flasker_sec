from flask import Flask, render_template, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

#  Create a Flask Instance
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretversion'
# Add Database Connection
# Old SQLite DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///codemy.db'
#  New MySQL DB
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost/name'

db = SQLAlchemy(app)


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(150), nullable=False, unique=True)
    favorite_color = db.Column(db.String(120))
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Name %r>' % self.name

# db.drop_all()
# db.create_all()

class UserForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    favorite_color = StringField('Favorite Color')
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
        return render_template("update_to_username.html", form=form, update_db_user=update_db_user)

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
            user = Users(name=form.name.data, email=form.email.data, favorite_color=form.favorite_color.data)
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        form.name.data = ''
        form.email.data = ''
        form.email.favorite_color = ''
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