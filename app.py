from flask import Flask, g
from flask import render_template, flash, redirect, url_for
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_bcrypt import check_password_hash

import models
# import forms

DEBUG = True
PORT = 8000

app = Flask(__name__)
app.secret_key = 'bojangles.yum'

login_manager = LoginManager()
## sets up our login for the app
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(userid):
    try:
        return models.User.get(models.User.id == userid)
    except models.DoesNotExist:
        return None


@app.before_request
def before_request():
    """Connect to the database before each request."""
    g.db = models.DATABASE
    g.db.connect()


@app.after_request
def after_request(response):
    """Close the database connection after each request."""
    g.db.close()
    return response


@app.route('/',methods=["POST"])
def index():
    models.User.create_user()




if __name__ == '__main__':
    models.initialize()
    try:
        models.User.create_user(
            username='firstUser',
            email="first@user.com",
            password='password',
            admin=True
            )
    except ValueError:
        pass

    app.run(debug=DEBUG, port=PORT)
