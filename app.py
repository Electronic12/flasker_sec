from flask import Flask, render_template, flash, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, logout_user, current_user, LoginManager, UserMixin, login_user
from forms import LoginForm, UserForm, PasswordForm, NamerForm, PostForm

#  Create a Flask Instance
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretversion'
# Add Database Connection
# Old SQLite DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///codemy.db'
#  New MySQL DB
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost/name'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

@app.route('/date/')
def date_for_json():
    favorite_games = {
        "Jora": "Futbol",
        "Kerwen": "Woleybol",
        "Mergen": "Judo"
    }
    return favorite_games
    # return {"Date": date.today() }

class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), nullable=False, unique=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(150), nullable=False, unique=True)
    favorite_color = db.Column(db.String(120))
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    password_hash = db.Column(db.String(120))
    posts = db.relationship('Posts', backref='poster')

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

class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    content = db.Column(db.Text(255))
    # author = db.Column(db.String(120))
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    slug = db.Column(db.String(255)) 
    poster_id = db.Column(db.Integer, db.ForeignKey(Users.id))

# db.drop_all()
# db.create_all()

@app.route('/login/', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password_hash, form.password.data):
                login_user(user)
                flash('Login successfully!!')
                return redirect(url_for('dashboard'))
            else:
                flash('Wrong password - try again')
        else:
            flash('This user doesnot ex')
   

    return render_template('login.html', form=form)

@app.route('/logout/', methods= ['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash('Logout successfully!!!')
    return redirect(url_for('login'))

@app.route('/dashboard/', methods = ['GET', 'POST'])
@login_required
def dashboard():
    form = UserForm()
    id = current_user.id
    update_db_user = Users.query.get_or_404(id)
    if request.method == 'POST':
        update_db_user.name = request.form['name']
        update_db_user.username = request.form['username']
        update_db_user.email = request.form['email']
        update_db_user.favorite_color = request.form['favorite_color']
        try:
            db.session.commit()
            flash("User update succsesfull")
            return render_template("dashboard.html", form=form, update_db_user=update_db_user)

        except Exception as ex:
            flash("Error!")
            return render_template("dashboard.html", form=form, update_db_user=update_db_user)

    else:
        return render_template("dashboard.html", form=form, update_db_user=update_db_user, id=id)

@app.route('/posts/<int:id>/')
def post(id):
    post = Posts.query.get_or_404(id)
    return render_template('post.html', post= post)

@app.route('/posts/')
def posts():
    posts = Posts.query.order_by(Posts.date_posted)
    return render_template('posts.html', posts= posts)

#  Posts Add 
@app.route('/add_post/', methods=['GET', 'POST'])
def add_post():
    form = PostForm()

    if form.validate_on_submit():
        post = Posts(title=form.title.data, author=form.author.data, slug=form.slug.data, content=form.content.data)
        form.title.data = ''
        form.author.data = ''
        form.content.data = ''
        form.slug.data = ''

        db.session.add(post)
        db.session.commit()

        flash('Blog Post Added Successfully')
    return render_template("add_post.html", form=form)

@app.route('/posts/edit/<int:id>/', methods=['GET', 'POST'])
def edit_post(id):
    post = Posts.query.get_or_404(id)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.author = form.author.data
        post.content = form.content.data
        post.slug = form.slug.data
        db.session.add(post)
        db.session.commit()
        flash('Post updated succsesfully.')
        return redirect(url_for('post', id=post.id))
    form.title.data = post.title
    form.author.data = post.author
    form.slug.data = post.slug
    form.content.data = post.content
    return render_template('edit_post.html', form=form)


@app.route('/update/<int:id>/', methods=['GET', 'POST'])
@login_required
def update(id):
    form = UserForm()
    update_db_user = Users.query.get_or_404(id)
    if request.method == 'POST':
        update_db_user.name = request.form['name']
        update_db_user.username = request.form['username']
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

@app.route('/posts/delete/<int:id>/')
def delete_post(id):
    post_to_delete = Posts.query.get_or_404(id)
    try:
        db.session.delete(post_to_delete)
        db.session.commit()
        flash('Post was deleted successfully')
        posts = Posts.query.order_by(Posts.date_posted)
        return render_template('posts.html', posts=posts)
    
    except:
        flash('There was an error deleting the post!')
        posts = Posts.query.order_by(Posts.date_posted)
        return render_template('posts.html', posts=posts)

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
            user = Users(username= form.username.data, name=form.name.data, email=form.email.data, favorite_color=form.favorite_color.data, password_hash=hashed_pw)
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        form.name.data = ''
        form.username.data = ''
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