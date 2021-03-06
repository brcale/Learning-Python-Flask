from flask import Flask, render_template, url_for, flash, redirect
from sqlalchemy import create_engine
from forms import RegistrationFrom, LoginForm
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app=Flask(__name__)
app.config['SECRET_KEY'] = '5961cf989b23694509406f0c9d5c9f86'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///site.db'
db=SQLAlchemy(app)

class User(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String(20),unique=True,nullable=False)
    email = db.Column(db.String(120), unique=False, nullable=False)
    password=db.Column(db.String(60),nullable=False)
    posts=db.relationship('Post',backref='author',lazy=True)

    def __repr__(self):
        return f"User('{self.username}','{self.email}')"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content=db.Column(db.Text,nullable=False)
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)

    def __repr__(self):
        return f"User('{self.title}','{self.date_posted}')"

posts=[
    {
    'author':'Bruno Cale',
    'title':'Blog post 1',
    'content':'First post content',
    'date_posted':'February 28, 2020'
    },
    {
    'author':'Luka Maric',
    'title':'Blog post 2',
    'content':'Second post content',
    'date_posted':'February 28, 2020'
    }
]

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts=posts)

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/register", methods=['GET','POST'])
def register():
    form=RegistrationFrom()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html',title='Register',form=form)

@app.route("/login", methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.username.data == 'bruno' and form.password.data == '123':
            flash(f'Hello {form.username.data}!','success')
            return redirect(url_for('home'))
        else:
            flash('Login Failed. Please check username and password and try again.','danger')
    return render_template('login.html',title='Login', form=form)

if __name__=="__main__":
    app.run(debug=True)
