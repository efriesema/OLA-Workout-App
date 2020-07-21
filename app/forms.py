from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError, NumberRange
from app.models import Team,Workout
import sys

  
class LoginForm(FlaskForm):
    team_name = StringField('Team name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class EntryForm(FlaskForm):
    athlete_id = SelectField('Athlete ID', choices= [('jallen02','jallen02'), ('thicks04','thicks04'),('lmbamo','lmbamo')] ,validators=[DataRequired()])
    exercise_name = SelectField('Exercise', choices= [('BenchPress','BenchPress'), ('Squats', 'Squats'),('Lat Pull Down', 'Lat Pull Down')] , validators=[DataRequired()])
    reps = IntegerField('Reps', validators=[DataRequired()])
    weight = IntegerField('Weight', validators=[DataRequired()])
    submit = SubmitField('Enter Exercise Data')

class WorkoutForm(FlaskForm):
    submit = SubmitField('Add New Exercise')


class RegistrationForm(FlaskForm):
    team_name = StringField('Team name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    team_size = IntegerField('Team Size')
    trainer = StringField( 'Trainer name', validators=[DataRequired()])
    trainer_email = StringField( 'Trainer email address', validators=[DataRequired(),Email()])
    athlete_userids = StringField('Athletes User IDs' )
    submit = SubmitField('Register')

    def validate_username(self, team_name):
        team = Team.query.filter_by(team_name=team_name.data).first()
        if team is not None:
            raise ValidationError('Please use a different team name.')
