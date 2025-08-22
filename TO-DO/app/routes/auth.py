from flask import render_template, redirect, request, url_for, flash, Blueprint, session
from app.models import Credentials
from app import db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        existing_user = Credentials.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists.', 'danger')
            return redirect('/register')
        
        new_user = Credentials(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        flash('Registered Successfully', 'success')
        return redirect('/login')
        
    return render_template('register.html')
    
    

    
@auth_bp.route('/login', methods = ['GET', "POST"])
def login():
    if request.method == "POST" :
        username = request.form.get("username")
        password = request.form.get("password")
        
        user = Credentials.query.filter_by(username=username, password=password).first()

        if user:
            session['user'] = username
            flash('Login Successfully', 'success')
            return redirect(url_for('tasks.view_tasks'))
        else :
            flash("Invalid usename or password")
            flash("If you are new click Register!!!")
    return render_template('login.html')


@auth_bp.route('/logout')
def logout():
    session.pop('user', None)
    flash('Logout Successfully', 'info')
    return redirect(url_for('auth.login'))
    