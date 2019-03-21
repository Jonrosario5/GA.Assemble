from flask import Flask, g
from flask import render_template, flash, redirect, url_for, request
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_bcrypt import check_password_hash

import models
import forms
import json

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
    g.user = current_user


@app.after_request
def after_request(response):
    """Close the database connection after each request."""
    g.db.close()
    return response

@app.route('/')
def index():
    return render_template('landing.html')

@app.route('/main')
def main():
    with open('topics.json') as topics_data:
        topics = json.load(topics_data)
        with open('events.json') as events_data:
            events = json.load(events_data)
            return render_template('main.html', topics=topics, events=events)

@app.route('/signup',methods=["GET","POST"])
def signup():
    form = forms.RegisterForm()
    if form.validate_on_submit():
        flash("Successful signup!",'success')
        models.User.create_user(
            username=form.username.data,
            fullname=form.fullname.data,
            email=form.email.data,
            password=form.password.data
        )
        return redirect(url_for('index'))
    topics = models.Topic.select()
    return render_template('register.html', form=form,topics=topics)

@app.route('/login', methods=('GET','POST'))
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        try:
            user = models.User.get(models.User.email == form.email.data)
        except models.DoesNotExist:
            flash("Your email doesn't exist")
        else:
            if check_password_hash(user.password, form.password.data):
                ## creates session
                login_user(user)
                flash("You've been logged in", "success")
                user_id = user.id
                
                return redirect(url_for('user_profile'))
            else:
                flash("your email or password doesn't match", "error")
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You've been logged out", 'success')
    return redirect(url_for('index'))

@app.route('/topic', methods=('GET','POST'))
def topic():
    form=forms.TopicForm()
    if form.validate_on_submit():
        flash("Successful signup!",'success')
        models.Topic.create_topic(
            name=form.name.data
        )
        return redirect(url_for('index'))
    return render_template('topic.html',form=form)



@app.route('/event', methods=('GET', 'POST'))
def event():
    # passes list of topics for dropdown menu
    topics = models.Topic.select()
    # event form
    eventForm=forms.EventForm()
    if eventForm.validate_on_submit():

        models.Event.create_event(
            title=eventForm.title.data,
            event_time=request.form.get('event_time'),
            location=eventForm.location.data,
            details=eventForm.details.data )

        event = models.Event.get(models.Event.title == eventForm.title.data)

        models.User_Events.create_user_event(
            user=g.user._get_current_object(),
            event=event,
            isHost=True
        )
        flash('Event created', 'success')
        return redirect(url_for('index'))
    return render_template('event.html', form=eventForm, topics=topics)              



@app.route('/user',methods=["GET","POST","DELETE","PUT"])
def user_profile():
    user = g.user._get_current_object()
    user_id = user.id
    topics = models.Topic.select()
    user_topics = models.User_Topics.select(models.User_Topics.user == user_id)
    user_events = models.User_Events.select(models.User_Events.user == user_id)

    form=forms.User_Topics()
    if form.validate_on_submit() and request.method == "POST":
        print(topics)
    else:
        print('nope')


    return render_template('profile.html',user_events=user_events,user_topics=user_profile,user=user, topics=topics,form=form)






if __name__ == '__main__':
    models.initialize()

    app.run(debug=DEBUG, port=PORT)
