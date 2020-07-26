from flask import render_template, flash, redirect, url_for, request
from werkzeug.urls import url_parse
from flask_login import current_user, login_user,logout_user, login_required
from app import app,db
from app.forms import LoginForm, EntryForm, WorkoutForm, RegistrationForm, TeamProfileForm
from app.models import Team, Workout
from datetime import datetime
import sys
import json


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title="Workout Data Entry App | Athletic Department | University of Nevada, Las Vegas")

@app.route('/workout',methods=['GET','POST'])
@login_required
def workout():
    """
    exercises  = [{'athlete_id': "jallen02" , 'exercise_name': 'Bench Press', 'parameters' : '[Reps, Weight]', 'entries' : '[10,175]', "time":'09:23:01'},
            {'athlete_id': "thicks04" , 'exercise_name': 'Bench Press', 'parameters' : '[Reps, Weight]', 'entries' :'[10,185]', "time":'09:25:01' },
            {'athlete_id': "jallen02" , 'exercise_name': 'Bench Press', 'parameters' : '[Reps, Weight]', 'entries' :'[8,195]', "time":'09:27:01'},
            {'athlete_id': "thicks04" , 'exercise_name': 'Bench Press', 'parameters' : '[Reps, Weight]', 'entries' :'[8,205]', "time":'09:29:01'}]"""
    exercises = Workout.query.all()  #only request exercises logged by current team
    for exercise in exercises:
        exercise.parameters = exercise.parameters[1:-1].split(",")
        exercise.entries = exercise.entries[1:-1].split(",")
    
    print("You have entered the workout page.",file =sys.stderr)
    print (exercises)
    form = WorkoutForm()
    if form.is_submitted():
        return redirect(url_for('entry'))
    dateString =  datetime.utcnow().strftime("%d-%b-%Y")
    return render_template('workout.html', title="Workout Data Entry App", date = dateString , exercises=exercises, form=form)


@app.route('/entry', methods= ['GET','POST'])
@login_required
def entry():
    print("You are in entry now")
    form = EntryForm()
    dateString =  datetime.now().strftime("%d-%b-%Y")
    team_roster= current_user.athlete_userids[1:-1].split(",")  #Take the athlete_userids string and split it into a list of athletes
    if form.validate_on_submit():
        if form.weight.data is None:
            flash('Weights must be a valid Integer')
            return redirect(url_for('entry'))
        if form.weight.data is None:
            flash('Reps must be a valid Integer')
            return redirect(url_for('entry'))
        new_entry =Workout(athlete_id= form.athlete_id.data, exercise_name= form.exercise_name.data, parameters= '[' +form.weight.name + ',' + form.reps.name + ']',
                entries = '[' +str(form.weight.data) + ', ' + str(form.reps.data) + ']', timestamp = datetime.utcnow(), team_id = current_user.id)
        print( new_entry, file=sys.stderr)
        db.session.add(new_entry)
        db.session.commit()
        return redirect(url_for('workout'))
    return render_template('entry.html', title="Exercise Entry Form",  team=team,  date= dateString, form=form)


@app.route('/login',methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        team= Team.query.filter_by(username=form.username.data).first()
        if team is None :
            flash('Invalid username')
            print("No team with that username exists.", file=sys.stderr)
            return redirect(url_for('login'))
        if not team.check_password(form.password.data) :
            flash('Invalid password')
            print("Password invalid.", file=sys.stderr)
            return redirect(url_for('login'))
        login_user(team, remember = form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        team = Team(username = form.username.data,team_name=form.team_name.data,  trainer=form.trainer.data, 
                    trainer_email = form.trainer_email.data, team_size = form.team_size.data, athlete_userids = form.athlete_userids.data)
        team.set_password(form.password.data)
        db.session.add(team)
        db.session.commit()
        flash('Congratulations, your team is now registered!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/team_profile')
@login_required
def team_profile():
    current_team = Team.query.filter_by(username=current_user.username).first_or_404()
    dateString =  datetime.now().strftime("%d-%b-%Y")
    form = TeamProfileForm
    team_roster= current_user.athlete_userids[1:-1].split(",")  #Take the athlete_userids string and split it into a list of athletes
    return render_template('team_profile.html', current_team=current_team, form=form, date=dateString, team_roster=team_roster)