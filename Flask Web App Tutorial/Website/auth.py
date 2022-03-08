from flask import Blueprint,render_template,request,flash,redirect,url_for
from .models import User
from werkzeug.security import generate_password_hash,check_password_hash
#hash are used to secure the password,  to not store it as plain text
# a hash function is a 1 way function, it does not have an inverse
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth',__name__)

@auth.route('/login', methods = ['GET','POST'])
def login():
    if request.method =="POST": # this is incase we are actually signing in and not just getting the page
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email = email).first() #scan through and  filter all of the users that have this email
        if user: # if we found the user
            if check_password_hash(user.password,password): # if they are the same
                flash('Logged in successfully!',category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exit.',category='error')

    return render_template("login.html", user = current_user)

@auth.route('/logout')
@login_required # makes sure that we cant access this page unless the user is logged in (not necessary though)
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
    

@auth.route('/sign-up', methods = ['GET','POST'])
def sign_up():
    if request.method=='POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists',category='error')
        elif len(email) <4 : 
            flash('Email must be greater than 4 characters', category = 'error')
        elif len(first_name) <2:
            flash('First name must ge greater than 1 chracter.', category='error')
        elif password1 != password2:
            flash('Password don\'t match,',category='error' )
        elif len(password1)<7:
            flash('Password must be at least 7 characters.',category='error')
        else:
            new_user = User(email = email,first_name = first_name,password=generate_password_hash(password1, method='sha256'))
            #sha256 is a hashing algorithm
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember = True)
            flash('Account created!',category='success')
            return redirect(url_for("views.home"))

    return render_template("sign_up.html", user = current_user)