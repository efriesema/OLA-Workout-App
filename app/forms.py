from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, IntegerField, DecimalField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError, NumberRange
from wtforms_dynamic_fields import WTFormsDynamicFields 
from app.models import Team,Workout,Exercise

import sys

  
class LoginForm(FlaskForm):
    username = StringField('Team name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class EntryForm(FlaskForm):
    athlete_id = SelectField('Athlete ID', validators=[DataRequired()])
    exercise_name = SelectField('Exercise',  validators=[DataRequired()],  id='select_ex')
    submit = SubmitField('Choose Athlete and Exercise')

    def __init__(self, names, athletes):
        super(EntryForm, self).__init__()
        self.exercise_name.choices = names
        self.athlete_id.choices = athletes

class RepsWeightForm(FlaskForm):
    reps = IntegerField('Reps', validators=[DataRequired(), NumberRange(min=1)])
    weight = IntegerField('Weight', validators=[DataRequired(), NumberRange(min=1)])
    rpe = IntegerField('RPE(6-20)', validators=[DataRequired(),NumberRange(min=6,max=20)])
    pain_area = SelectField('Pain Location', choices=[('None','None'),('Head','Head'),('Neck','Neck'), ('Chest','Chest'),('Upper Back','Upper Back'),
            ('Lower Back','Lower Back'), ('Abs','Abs'),('Groin','Groin'),('Arms','Arms'),('Legs','Legs')], validators=[DataRequired()])
    submit = SubmitField('Enter Data')


class RepsForm(FlaskForm):
    reps = IntegerField('Reps', validators=[DataRequired(), NumberRange(min=1)])
    rpe = IntegerField('RPE(6-20)', validators=[DataRequired(),NumberRange(min=6,max=20)])
    pain_area = SelectField('Pain Location', choices=[('None','None'),('Head','Head'),('Neck','Neck'), ('Chest','Chest'),('Upper Back','Upper Back'),
            ('Lower Back','Lower Back'), ('Abs','Abs'),('Groin','Groin'),('Arms','Arms'),('Legs','Legs')], validators=[DataRequired()])
    submit = SubmitField('Enter Data')


class RepsAccelForm(FlaskForm):
    reps = IntegerField('Reps', validators=[DataRequired(), NumberRange(min=1)])
    acceleration = DecimalField('Acceleration', validators=[DataRequired()])
    rpe = IntegerField('RPE(6-20)', validators=[DataRequired(),NumberRange(min=6,max=20)])
    pain_area = SelectField('Pain Location', choices=[('None','None'),('Head','Head'),('Neck','Neck'), ('Chest','Chest'),('Upper Back','Upper Back'),
            ('Lower Back','Lower Back'), ('Abs','Abs'),('Groin','Groin'),('Arms','Arms'),('Legs','Legs')], validators=[DataRequired()])
    submit = SubmitField('Enter Data')


class WorkoutForm(FlaskForm):
    submit = SubmitField('Add New Exercise')


class BiometricForm(FlaskForm):
    athlete_id = SelectField('Athlete ID', validators=[DataRequired()])
    weight = DecimalField('Weight(lbs)', validators=[DataRequired()])
    height = DecimalField('Height(ins)', validators=[DataRequired()])
    submit = SubmitField('Enter Bio Data')

    def __init__(self, athletes):
        super(BiometricForm, self).__init__()
        self.athlete_id.choices = athletes

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
    submit = SubmitField('Go Back')


class CustomEntryForm(FlaskForm):
    reps = IntegerField('Reps', validators=[DataRequired(), NumberRange(min=1)])
    acceleration = DecimalField('Acceleration', validators=[DataRequired()])
    weight = IntegerField('Weight', validators=[DataRequired(), NumberRange(min=1)])
    rpe = IntegerField('RPE(6-20)', validators=[DataRequired(),NumberRange(min=6,max=20,message='You must choose an RPE value between 6-20')])
    pain_area = SelectField('Pain Location', choices=[('None','None'),('Head','Head'),('Neck','Neck'), ('Chest','Chest'),('Upper Back','Upper Back'),
            ('Lower Back','Lower Back'), ('Abs','Abs'),('Groin','Groin'),('Arms','Arms'),('Legs','Legs')], validators=[DataRequired()])
    submit = SubmitField('Enter Data')
      


