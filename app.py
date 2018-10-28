from flask import Flask, render_template, json, request, redirect, url_for, flash
from flask_moment import Moment 
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Email, Length

app = Flask(__name__)
app.config['SECRET_KEY'] = 'tqnty%^5889@GCGHcgcGcfgbJGFgfjUIy8yy85685TGYGH56'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://///path/to/your/db/users.db'

db = SQLAlchemy(app)

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/showSignUp',methods=['GET','POST'])
def showSignUp():
    if request.method == 'POST':
        try:
            _name = request.form['inputName']
            _email = request.form['inputEmail']
            _password = request.form['inputPassword']

            print(_name, _email, _password)
            if _name and _email and _password:
                _hashed_password = generate_password_hash(_password, method = "sha256")
                new_user = Users(name = _name, email = _email, password = _hashed_password)
                db.session.add(new_user)
                db.session.commit()
                return redirect(url_for('login'))
            else:
                return redirect(url_for('showSignUp'))
        except Exception:
            return
    return render_template('signup.html')

@app.route('/login',methods=['GET','POST'])
def login():
    error = None
    if request.method == 'POST':
        _email = request.form['inputEmail']
        _password = request.form['inputPassword']
        user = Users.query.filter_by(email = _email ).first()
        if check_password_hash(user.password, _password):
            print("user",user.name)
            return redirect(url_for('main'))
        else:
            error = 'Invalid credentials'
            return redirect(url_for('showSignUp'))
    return render_template('login.html', error=error)


class Users(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(50))
    password = db.Column(db.String(80))


if __name__ == "__main__":
    app.run(port=8080)
 