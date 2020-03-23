from app import app, forms
from flask import render_template, request

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

        return render_template('thanks.html', feedback=feedback)

    return render_template('feedback.html', form=form)