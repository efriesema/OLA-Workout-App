from app import app, db
from app.models import Team, Workout, Exercise


@app.shell_context_processor
def make_shell_context():
    return {'db': db , 'Team': Team, 'Workout' : Workout, 'Exercise' : Exercise}
