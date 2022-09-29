from flask import Flask, render_template, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, EmailField
from wtforms.validators import DataRequired, Email

app = Flask(__name__)
app.config['SECRET_KEY'] = 'top secret'

# Extensions
bootstrap = Bootstrap(app)
moment = Moment(app)

# Form to collect name and email
class UserForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    email = EmailField('What is your UofT Email address?', validators=[DataRequired()])
    submit = SubmitField('Submit')


# Default path
@app.route('/', methods=['GET', 'POST'])
def index():
    form = UserForm()
    if form.validate_on_submit():
        # Process name
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash('Looks like you have changed your name!')
        session['name'] = form.name.data

        # Process email
        session['email_entered'] = True
        old_email = session.get('email')
        current_email = form.email.data
        session['email'] = current_email
        # Validate current_email
        if current_email is not None and 'utoronto' in current_email:
            session['email_valid'] = True
        else:
            session['email_valid'] = False

        if old_email is not None and current_email != old_email:
            flash('Looks like you have changed your email!')

        return redirect(url_for('index'))
    return render_template('index.html', form=form, name=session.get('name'), 
    email=session.get('email'), email_valid = session.get('email_valid'), email_entered = session.get('email_entered'))

@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)


# Error handling
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500