from flask import render_template, flash, redirect, url_for, session, request, logging
from app import app, db, bcrypt
from app.forms import RegisterForm, LoginForm, UpdateAccountForm, PostForm
from app.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required   # importing decorated func from models

@app.route('/')
@app.route('/home')
def home():
    posts = Post.query.all() 
    return render_template('home.html', posts=posts) 

@app.route('/about')
def about():
    return render_template('about.html')

# register route
@app.route('/register', methods=['POST', 'GET'])
def register():
    if current_user.is_authenticated:   # when user is logged already redirect
        return redirect(url_for('home'))

    form = RegisterForm()
    # checking for data validation
    if form.validate_on_submit():
        # encrypting our password
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)    # adding user to db
        db.session.commit()   # submitting to db
    # success message
        flash(f'Account created! You can now login', 'success')    # success msg for user info submitted
        return redirect(url_for('login'))

    return render_template('register.html', title='Register', form=form)

# login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:   # when user is logged already redirect
        return redirect(url_for('home'))
    form = LoginForm()
    # checking for data validation
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next') 
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash(f'Login Unsuccessful, Check your email or password', 'danger')
    return render_template('login.html', title='Login', form=form)

# logout route
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

# account route 
@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()

        flash(f'Account Updated', 'success')

        return redirect(url_for('account'))

    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='images/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)

# new posts
@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit() 
        flash(f'Post created!', 'success')
        return redirect(url_for('home'))

    return render_template('create_post.html', title='New Post', form=form)