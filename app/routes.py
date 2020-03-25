from app import app, forms
from flask import render_template, request
from app.models import Feedback
from app import db

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    form = forms.FeedbackForm()

    if form.validate_on_submit():
        name = form.name.data
        text = form.text.data

        feedback = {'name':name, 'text':text}

        f = Feedback(name=name, text=text)
        db.session.add(f)
        db.session.commit()

        return render_template('thanks.html', feedback=feedback)

    return render_template('feedback.html', form=form)


@app.route('/show')
def show_feedbacks():
    feedbacks = Feedback.query.all()
    return render_template('show.html', feedbacks=feedbacks)
