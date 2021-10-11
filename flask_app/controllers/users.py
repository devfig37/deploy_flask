from flask_app import app
from flask import render_template, redirect, session, request, flash
from flask_app.models.user import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/register', methods=['POST'])
def register():
    data = {
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email": request.form["email"],
        "password": request.form["password"],
        "confirm_password": request.form["confirm_password"],
    }
    valid = User.validate_user(data)
    print(valid)
    if valid:
        hashed_password = bcrypt.generate_password_hash(
            request.form['password'])
        print(request.form['password'])
        print(hashed_password)
        data['hashed_password'] = hashed_password
        user = User.create_user(data)
        session['user_id'] = user
        print('Logged in to your dashboard!')
        return redirect('/dashboard')
    return redirect('/')


@app.route('/login', methods=['POST'])
def login():
    user = User.get_email(request.form)

    if not user:
        flash('Invalid email or password!')
        return redirect('/')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash('Invalid email or password!')
        return redirect('/')
    session['user_id'] = user.id
    print('Logged into your dashboard!')
    return redirect('/dashboard')


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
