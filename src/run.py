from flask import Flask, render_template, redirect, url_for, request
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
import sirope
from src.models import User, Paper, Post

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Sirope setup
s = sirope.Sirope()


@login_manager.user_loader
def load_user(user_id):
    user = s.find_first(User, lambda u: u.username == user_id)
    return user


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = s.find_first(User, lambda u: u.email == email and u.password == password)
        if user:
            login_user(user)
            return redirect(url_for('index'))
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/')
@login_required
def index():
    return f'Hello, {current_user.username}!'


if __name__ == '__main__':
    app.run(debug=True)
