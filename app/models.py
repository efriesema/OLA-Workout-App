from datetime import datetime
from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from hashlib import md5


@login.user_loader      ##Necessary loader function to take login id string and convert it into int
def load_user(id):
    return Team.query.get(int(id))


class Team(UserMixin, db.Model):  
    ##  Decribes Team SQLAlchemy database model in terms of fields, properties and relationships,  Team is equivalent of User in many other applications
    ##   because workout data will be entered most often in team sessions as opposed to individual workouts.  Although there is no reason a single user could not 
    ##  use this system for a personal workout
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    team_name = db.Column(db.String(64), index=True)
    team_size = db.Column(db.Integer)
    trainer = db.Column(db.String(64))
    trainer_email = db.Column(db.String(120), index=True)
    password_hash = db.Column(db.String(128))
    athlete_userids = db.Column(db.String(140))    # A string representing a list of athlete_id strings
    workouts = db.relationship('Workout', backref='team', lazy='dynamic')
    
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    

    def check_password(self, password):
        return check_password_hash(self.password_hash,password)

    
    def __repr__(self):
        return '<User {}, Team {}, Team ID {}, Trainer {}, Email {}, Athlete User IDs{}>'.format(self.username, self.team_name, self.id, self.trainer,self.trainer_email, self.athlete_userids)

    def get_names(self):
        ## returns a list of unique exercise names choice tuples from Exercise table
        names = self.query.filter_by(id=current_user.team_id).athlete_userids.first()
        return [(i,i) for i in [value for value, in names]]

class Workout(db.Model):
    ## Database schema for a workout.  A workout being defined as a series of exercises  by multiple athletes on the same team
    id = db.Column(db.Integer, index=True, primary_key=True)
    athlete_id = db.Column(db.String(30))
    exercise_name = db.Column(db.String(50))
    parameters = db.Column(db.String(100))          # A string representing a list of exercise parameters
    entries = db.Column(db.String(100))             # A string representing a list of exercise parameter values
    timestamp = db.Column(db.DateTime, index=True,default=datetime.utcnow())
    team_id =db.Column(db.Integer, db.ForeignKey('team.id'))


    def __repr__(self):
        return '<Exercise {}, Team_ID {} >'.format(self.exercise_name, self.team_id)

class Exercise(db.Model):
    ## Database schema for exercises based on parameters
    id = db.Column(db.Integer, index=True, primary_key=True)
    exercise_name = db.Column(db.String(30))
    parameter = db.Column(db.String(30))
    value = db.Column(db.String(20))
    unit = db.Column(db.String(20))


    def get_names():
        ## returns a list of unique exercise names choice tuples from Exercise table
        names = db.session.query(Exercise.exercise_name).distinct() 
        return [(i,i) for i in [value for value, in names]]


    def __repr__(self):
        return '< Exercise {}, Parameter {}, Value {}, Unit {} >'.format(self.exercise_name, self.parameter, self.value, self.unit)
