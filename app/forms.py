from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired

class FeedbackForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    text = TextAreaField('Feedback', validators=[DataRequired()])
    submit = SubmitField('Submit')