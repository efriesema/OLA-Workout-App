from datetime import datetime
from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from hashlib import md5

"""
@login.user_loader      ##Necessary loader function to take id string and convert it into int
def load_user(id):
    return Team.query.get(int(id))
"""

class Team(UserMixin, db.Model):  
    ##  Decribes Team SQLAlchemy database model in terms of fields, properties and relationships,  Team is equivalent of User in many other applications
    ##   because workout data will be entered most often in team sessions as opposed to individual workouts.  Although there is no reason a single user could not 
    ##  use this system for a personal workout
    id = db.Column(db.Integer, primary_key=True)
    team_name = db.Column(db.String(64), index=True, unique=True)
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
        return '<Team {}, Trainer {}, Email {}>'.format(self.team_name, self.trainer,self.trainer_email)


class Workout(db.Model):
    ## Database schem for a workout.  A workout being defined as a series of exercises  by multiple athletes on the same team
    id = db.Column(db.Integer, index=True, primary_key=True)
    athlete_id = db.Column(db.String(30))
    exercise_name = db.Column(db.String(50))
    parameters = db.Column(db.String(100))          # A string representing a list of exercise parameters
    entries = db.Column(db.String(100))             # A string representing a list of exercise parameter values
    timestamp = db.Column(db.DateTime, index=True,default=datetime.utcnow())
    team_id =db.Column(db.Integer, db.ForeignKey('team.id'))

    def __repr__(self):
        return '<Exercise {}>'.format(self.exercise_name)
