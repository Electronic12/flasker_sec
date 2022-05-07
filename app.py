from xmlrpc.client import Boolean
from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

#  Create a Flask Instance
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretversion'

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

# Call to html file
@app.route('/')
def index():
    first_name = 'Kerwen'
    # second_name = '<strong>Abdullayew</strong>'
    second_name = 'Abdullayew'
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
    return render_template("name.html",
                            name=name, 
                            form=form)

if __name__ == '__main__':
    app.run(debug=True)