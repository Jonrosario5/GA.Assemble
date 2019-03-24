from flask import Flask, g
from flask import render_template, flash, redirect, url_for, request, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_bcrypt import check_password_hash
from peewee import fn
from peewee import *

import models
import forms
import json
from datetime import datetime

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
@app.route('/main/<topicid>', methods=['GET'])
def main(topicid=None):
    if topicid != None:
        events = models.Event.select().where(models.Event.topic_id == topicid)
    else:
        events = models.Event.select()
    topics = models.Topic.select(models.Topic.id, models.Topic.name, fn.COUNT(models.User_Topics.user_id).alias('num_of_followers')).join(models.User_Topics, JOIN.LEFT_OUTER, on=(models.Topic.id == models.User_Topics.topic_id)).group_by(models.Topic.id, models.Topic.name)
    eventForm=forms.EventForm()
    return render_template('main.html', topics=topics, events=events, form=eventForm)

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



@app.route('/event', methods=['POST'])
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
            details=request.form.get('details'),
            # details=eventForm.details.data,
            topic=request.form.get('topics'),
            created_by_id=g.user._get_current_object()
             )

        event = models.Event.get(models.Event.title == eventForm.title.data)

        models.User_Events.create_user_event(
            user=g.user._get_current_object(),
            event=event,
            isHost=True
        )
        flash('Event created', 'success')
        return redirect(url_for('main'))
    return render_template('event.html', form=eventForm, topics=topics) 


@app.route('/delete_event/<eventid>', methods=['GET', 'POST'])
def delete_event(eventid=None):
    user = g.user._get_current_object()

    if eventid !=None:
        delete_user_event = models.User_Events.delete().where(models.User_Events.user_id == user.id and models.User_Events.event_id == eventid)
        delete_user_event.execute()
        delete_this_event = models.Event.delete().where(models.Event.created_by_id == user.id and models.Event.id ==eventid)
        delete_this_event.execute()
        
        return redirect(url_for('user_profile'))
    return redirect('user')

@app.route('/attend/<eventid>', methods=['GET', 'POST'])
def attend_event(eventid=None):
    user_events_count = models.User_Events.select().where((models.User_Events.user_id == g.user._get_current_object().id) & (models.User_Events.event_id == eventid)).count()

    if eventid != None and user_events_count <= 0:
        models.User_Events.create_user_event(
            user=g.user._get_current_object(),
            event=eventid,
            isHost=False
        )
        return redirect(url_for('user_profile'))
    return redirect('main')


@app.route('/unattend/<eventid>', methods=['GET', 'POST'])
def unattend_event(eventid=None):   
    user = g.user._get_current_object()
    if eventid != None:
        unattend_this_event = models.User_Events.delete().where(models.User_Events.user_id == user.id and models.User_Events.event_id == eventid)
        unattend_this_event.execute()

        return redirect(url_for('user_profile'))
    return redirect('user')
    



@app.route('/user',methods=["GET","POST"])
@app.route('/user/<topicid>',methods=["GET","POST"])

# @login_required
def user_profile(topicid=None):
    user = g.user._get_current_object()
    user_id = user.id
    print("this is the user id",user_id)
    topics = models.Topic.select()
    event_form = forms.EventForm()
    form = forms.Edit_User_Form()
    user_topics = models.User_Topics.select().where(models.User_Topics.user_id == user.id) 
    user_events = models.User_Events.select().where(models.User_Events.user_id == user.id)
    attending_events = models.User_Events.select().where(models.User_Events.user == user_id, models.User_Events.isHost != True)
   

    if topicid != None:
        user_topics_count = models.User_Topics.select().where((models.User_Topics.user_id == user.id) & (models.User_Topics.topic_id == topicid)).count()
        if user_topics_count > 0:
            flash('Already Exists')
            print('Working')
            return redirect('user')

        else:
            models.User_Topics.create_usertopic(
            topic=topicid,
            user=user.id
            )
            return redirect('user')


    else:
        print("Hi")



    return render_template('profile.html',user_events=user_events,attending_events=attending_events,user_topics=user_topics,user=user, topics=topics,form=form, event_form=event_form)

@app.route('/usertopic/delete/<topicid>',methods=["GET","POST"])
def delete_user_topic(topicid=None):
    user = g.user._get_current_object()
    user_id = user.id
    if topicid != None:
        delete_topic = models.User_Topics.delete().where(models.User_Topics.user_id == user.id and models.User_Topics.topic_id == topicid)
        delete_topic.execute()

        return redirect('user')

@app.route('/userupdate', methods=['GET','POST'])
def edit_user():
    update = forms.Edit_User_Form()

    if update.validate_on_submit:
        print(update.fullname)
        update_user = (models.User.update(
            {models.User.fullname:update.fullname.data,
            models.User.username:update.username.data})
            .where(models.User.id == g.user._get_current_object().id))
        update_user.execute()

        return redirect('user')

@app.route('/update_user_event', methods=['GET','POST'])
def edit_user_event():
    update = forms.EventForm()

    if update.validate_on_submit:
        update_user = (models.Event.update(
            {models.Event.title:update.title.data,
            models.Event.location:update.location.data,
            models.Event.details:update.details.data
            })
            .where(models.Event.id == update.event_id.data))
        update_user.execute()

        return redirect('user')



if __name__ == '__main__':
    models.initialize()
    # app.jinja_env.auto_reload = True
    # app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=DEBUG, port=PORT)
