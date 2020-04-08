from flaskblog.models import User, Post
from flask import render_template, url_for, flash, redirect, request
from flaskblog.forms import RegistrationForm, LoginForm
from flaskblog import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required

posts_array = [
    {
        'author': 'Sahil',
        'title': 'Blog-1',
        'content': 'This is blog 1',
        'date_posted': 'March 31, 2020'
    },
    {
        'author': 'Bot',
        'title': 'Blog-2',
        'content': 'This is blog 2',
        'date_posted': 'April 1, 2020'
    }
]


@app.route("/")
@app.route("/home")
def homepage():
    return render_template("index.html", posts=posts_array)


@app.route("/about")
def aboutpage():
    return render_template("about.html", title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('homepage'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been created! You can now login!', category='success')
        return redirect(url_for('login'))

    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('homepage'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash('You are now logged in!', category='success')
            return redirect(next_page) if next_page else redirect(url_for('homepage'))
        else:
            flash('login Unsuccessful. Please check credentials.', category='danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    flash('You are logged out successfully', category='info')
    return redirect(url_for('homepage'))


@app.route("/account")
@login_required
def account():
    return render_template('account.html', title='Account')
