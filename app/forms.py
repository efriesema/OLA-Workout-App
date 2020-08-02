from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError, NumberRange
from app.models import Team,Workout,Exercise
import sys

  
class LoginForm(FlaskForm):
    username = StringField('Team name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class EntryForm(FlaskForm):
    athlete_id = SelectField('Athlete ID', choices= [('jallen02','jallen02'), ('thicks04','thicks04'),('lmbamo','lmbamo')] ,validators=[DataRequired()])
    exercise_name = SelectField('Exercise', choices= [('BenchPress01','BenchPress01'), ('Squats01','Squats01'),('LatPullDown01','LatPullDown01')], validators=[DataRequired()],  id='select_ex')
    reps = IntegerField('Reps', validators=[DataRequired()])
    weight = IntegerField('Weight', validators=[DataRequired()])
    submit = SubmitField('Enter Exercise Data')

    def __init__(self, names):
        super(EntryForm, self).__init__()
        self.exercise_name.choices = names


class WorkoutForm(FlaskForm):
    submit = SubmitField('Add New Exercise')


class RegistrationForm(FlaskForm):
    username = StringField('User name', validators=[DataRequired(), Length(min=6, max=20, message='Please choose a username between 6 and 20 characters.') ])
    team_name = StringField('Team name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    trainer = StringField( 'Trainer name', validators=[DataRequired()])
    trainer_email = StringField( 'Trainer email address', validators=[DataRequired(),Email()])
    team_size = IntegerField('Team Size')    
    athlete_userids = StringField('Athlete User IDs' )
    submit = SubmitField('Register')


class TeamProfileForm(FlaskForm):
    username = StringField('User name')
    team_name = StringField('Team name')
    trainer = StringField('Trainer name')
    trainer_email = StringField( 'Trainer email address', validators=[Email()])
    team_size = IntegerField('Team Size')    
    athlete_userids = StringField('Athlete User IDs' )
    submit = SubmitField('Register')