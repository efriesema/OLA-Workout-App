from flask import render_template, flash, redirect, url_for, request
from werkzeug.urls import url_parse
from flask_login import current_user, login_user,logout_user, login_required
from wtforms import StringField
from wtforms_dynamic_fields import WTFormsDynamicFields 
from app import app,db
from app.forms import LoginForm, EntryForm, WorkoutForm, RegistrationForm, TeamProfileForm, RepsWeightForm, RepsForm, RepsAccelForm, BiometricForm, CustomEntryForm
from app.models import Team, Workout, Exercise
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
    exercises = Workout.query.filter_by(team_id=current_user.id).all()  # TODO: only request exercises logged by current team
    for exercise in exercises:
        exercise.parameters = exercise.parameters[1:-1].split(",")
        exercise.entries = exercise.entries[1:-1].split(",")
    
    print("You have entered the workout page.")
    print (exercises)
    form = WorkoutForm()
    if form.is_submitted():
        return redirect(url_for('entry'))
    dateString =  datetime.utcnow().strftime("%d-%b-%Y")
    return render_template('workout.html', title="Workout Data Entry App", date = dateString , exercises=exercises, form=form)


@app.route('/biometric', methods=['GET','POST'])
@login_required
def biometric():  
    team_roster= current_user.athlete_userids[1:-1].split(",")  #Take the athlete_userids string and split it into a list of athletes
    athlete_names = [(i,i) for i in team_roster]
    dateString =  datetime.now().strftime("%d-%b-%Y")
    form = BiometricForm(athlete_names)
    if form.validate_on_submit():
        return redirect(url_for('index'))
    return render_template('biometric.html', title="Biometrics Entry Form",  date= dateString, form=form)

@app.route('/entry', methods= ['GET','POST'])
@login_required
def entry():
    print("You are in entry now")  
    dateString =  datetime.now().strftime("%d-%b-%Y")
    team_roster= current_user.athlete_userids[1:-1].split(",")  #Take the athlete_userids string and split it into a list of athletes
    athlete_names = [(i,i) for i in team_roster]
    exercise_names = Exercise.get_names()
    form = EntryForm(exercise_names,athlete_names)
    
    if form.validate_on_submit():
        ex_name= form.exercise_name.data
        athlete_id= form.athlete_id.data.lstrip(' ')   #strips leading whitespaces from athlete_id
        return redirect(url_for('second',exercise_name=ex_name,athlete_id=athlete_id))     
    return render_template('entry.html', title="Exercise Entry Form",  date= dateString, form=form)

@app.route('/<exercise_name>/<athlete_id>', methods = ['GET','POST'])
@login_required
def second(exercise_name,athlete_id):
    if (exercise_name=="BenchPress01" or exercise_name =="DeadLift01"):
        form = RepsWeightForm() 
        page = 'repsweight.html'
    elif (exercise_name == "Burpies01"):
        form = RepsForm()
        page = 'reps.html'
    elif (exercise_name == "LatPullDown01"):
        form = RepsAccelForm()
        page = 'repsaccel.html'
    dateString =  datetime.now().strftime("%d-%b-%Y")
    if form.validate_on_submit():  
        print(f"Pain area data is [{form.pain_area.data}]")
        if (exercise_name =="BenchPress01" or exercise_name =="DeadLift01"):  
            prm_string = f'[{form.reps.name},{form.weight.name},{form.rpe.name},{form.pain_area.name}]'
            entry_string = f'[{form.reps.data},{form.weight.data},{form.rpe.data},{form.pain_area.data}]'           
        elif (exercise_name == "Burpies01"):  
            prm_string = f'[{form.reps.name},{form.rpe.name},{form.pain_area.name}]'
            entry_string = f'[{form.reps.data},{form.rpe.data},{form.pain_area.data}]'  
        elif (exercise_name == "LatPullDown01"):
            prm_string = f'[{form.reps.name},{form.acceleration.data},{form.rpe.name},{form.pain_area.name}]'
            entry_string = f'[{form.reps.data},{form.acceleration.data},{form.rpe.data},{form.pain_area.data}]' 
        new_entry =Workout(athlete_id=athlete_id, exercise_name= exercise_name, parameters= prm_string,
                entries = entry_string, timestamp = datetime.utcnow(), team_id = current_user.id)    
        db.session.add(new_entry)
        db.session.commit()
        return redirect(url_for('workout'))
    return render_template(page, title= "Exercise Entry Form",  date= dateString, form=form )


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


@app.route('/team_profile/<team_name>')
@login_required
def team_profile(team_name):
    team = current_user
    dateString =  datetime.now().strftime("%d-%b-%Y")
    form = TeamProfileForm()
    team_roster= current_user.athlete_userids[1:-1].split(",")  #Take the athlete_userids string and split it into a list of athletes
    return render_template('team_profile.html', team=team, form=form, date=dateString, team_roster=team_roster)

@app.route("/custom")
def custom():
    """
    Field list for exercise entry form
    0 = Reps (int)
    1 = Acceleration(Decimal)
    2 = Weight(int)
    3 = RPE(int)
    4 = Pain (Select)
    """
    form = CustomEntryForm()
    for field in form:
        print(field.name)
    removes = [1]        # list of fields you wish to remove from form 
    for i in removes:
        if (i==0):
            del form.reps
        elif (i==1):
            del form.acceleration
        elif (i==2):
            del form.weight
        elif (i==3):
            del form.rpe
        elif (i==4):
            del form.pain_area
    dateString =  datetime.now().strftime("%d-%b-%Y")
    return render_template('custom.html', title="Custom Entry Form",form=form,date = dateString)