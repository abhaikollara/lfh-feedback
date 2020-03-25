

_This might be a bit harder to follow if you haven't been in the 5-6PM batch since the contents of this follow directly from what was discussed in those sessions_


# Talking with databases

So far we looked at
- basic client-server model
- How to route urls to the proper views
- How to use templates to render HTML
- How to create forms (using flask-wtf)
- Receive data and use that data to construct new views.

This is pretty impressive. You deserve a pat on the back. But what we've gone through is still pretty limiting. Last time when we received data from the feedback form we used it to immediately create a thank you page that displayed the name and the feedback. We never really stored the data. The data was immediately processed and returned back. In fact, if we stop and restart our server, our app will have no idea about the feedback that was entered earlier. You can guess how this going to be a problem. With what we've covered so far, we cannot have, say, a login page. For that we'd at least need to store the usernames and  the corresponding passwords. 

For our example, if we need a page that shows all the feedbacks that have been entered until now, we would require a way to store the feedbacks.

So, what is the solution ? Enter databases. 

## Databases
Databases provide persistence to your data independent of your web app. They allow us to store and retrieve data efficiently. Now, databases themselves are an entire area of study. If you are a CS major, it is at least one semester worth of study. So I won't venture too deep into databases themselves. Partly, because it'll take up too much of our time and partly because we don't need to. For us, Flask, a few plugins and sql-alchemy is going to allow us to ignore a huge part of the complexity of managing a database.

Let's consider our use case. Our db will contain a table `feedback` with two columns: `name` and `text`. You can think of tables as glorified Excel sheets for now. Every row in that table will be an instance of a single feedback.

Whenever a user fills the feedback form, we capture the name and text and store it in a new row in the feedback table in our database. Similarly, whenever the user visits the `/show` page, we are going to retrieve all the feedbacks stored in the database and display it one by one.

## sql-alchemy
The kind of database that I mentioned above is called SQL databases. In order to store, modify and retrieve data from these databases we use a language called SQL. We too can write SQL commands to communicate with our databases, but it can be cumbersome for the programmer to mix Python and SQL together. It can also be an error prone process. This is where `sql-alchemy` comes in. `sql-alchemy` is what is known as an object relational mapper (ORM). It acts as an interface between Python and an SQL database. Through sql-alchemy you can write Python code in terms of objects and classes that automatically get translated to database commands. Moreover, sql-alchemy also allows you change the underlying database system without having to change the Python code.

## Show me some code
Let's do a quick run through of the required code. But before that you need to install a couple of packages
- `pip install flask-sqlalchemy`
- `pip install flask-migrate`

Once you've done that let's get started. First of all, we need to establish a link between Flask and our database.

### `app/config.py`
So head over to `config.py` and add the following lines
```python
basedir = os.path.abspath(os.path.dirname(__file__))
```
Add this to `Config` class
```python
SQLALCHEMY_DATABASE_URI  = 'sqlite:///'  + os.path.join(basedir, 'app.db')
SQLALCHEMY_TRACK_MODIFICATIONS  =  False
```

This simply establishes the location of our database. I suggest you find out own your own, what path is being sent here.

### `app/__init__.py`
Nothing much to explain here. Just see the code

### `app/models.py`
```python
from app import db

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=False, unique=True)
    text = db.Column(db.String(1000), index=False, unique=True)

    def __repr__(self):
        return '<Feedback {}>'.format(self.name)   
```

This is a new file we are going to create. Models are the equivalent of database tables on the python side. So, here we define our representation of `Feedback` table. The code is pretty self explanatory. The only additional thing here is the presence of an `id` column which is mandatory for any model. Also, Google what the `__repr__` is for.

Now that we've created a model. We need to "migrate" this into our database. Run the following commands in your command line
```python
flask db init
flask db migrate -m "feedback table"
flask db upgrade
```
This will actually create the `feedback` table in our database.

### `routes.py`
Phew, that's a lot of work and we haven't even gotten started with the real work. So far, we've establish the link between a database and created a table to contain the feedbacks. Now we get into the business of actually pushing data into the table.

#### Storing the data
We already know where we captured the form data. Previously we sent the data into a thanks page where it was displayed. We're still gonna do that, but this time we are also going to store the data into our newly created table.

```python
@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    form = forms.FeedbackForm()

    if form.validate_on_submit():
        name = form.name.data
        text = form.text.data

        feedback = {'name':name, 'text':text}
        
        #####################################
        f = Feedback(name=name, text=text). #
        db.session.add(f)                   # These three lines do the job
        db.session.commit()                 #
        #####################################
        
        return render_template('thanks.html', feedback=feedback)

    return render_template('feedback.html', form=form)
```
In the first of the new lines we create an object of the `Feedback` model that we earlier created. Then we add it to the db and commit. (We can later find out why adding and committing needs to separate). Your feedback is now stored into the database. Note that `sql-alchemy` takes care of generating the appropriate SQL commands that are required to push this data into the database. This is great (esp. if you're like me and don't know much SQL).

#### Retriving the data
Now that we've stored the data in our database. We'll learn how to retrieve them. Since we want to create a page to show the feedbacks that have already been given, we'll create a new route and view for this. We'll display it at `/show`. This is the view function:

```python
@app.route('/show')
def  show_feedbacks():
	feedbacks = Feedback.query.all()
	return render_template('show.html', feedbacks=feedbacks)
```

As you can see, we use `Feedback.query.all()` to retrieve all the feedbacks that are stored in the table. This list is then passed into the template shown below which displays them one by one.

> `query.all()` is probably the simplest database query (means search) I could imagine. We can certainly create more complex queries. You can query for feedbacks from a certain person. You can only query for feedbacks longer than 200 words etc. 
This can get even more complex when you have databases with multiple tables (most dbs do). Why would you need to have multiple tables ? Let's say you have implemented login and logged in users now provide feedback. Additionally the users provide additional information about themselves like age, address and email. It doesn't make sense to store these information in the same table as feedback. Instead we create a different table for users with user data and then link the user column of the feedback table with user table. This is called a relationship. Complex web apps can have hundreds of tables and as many relationships between them.


### `show.html`
```
{%extends "base.html"%} {% block content %}

<div>
	{%for fb in feedbacks%}
	<p>
		<b>{{fb.name}} says: </b>
	</p>
	<p>
		{{fb.text}}
	</p>
	{%endfor%}
</div>

{%endblock%}
```

That's it. We now have a form that takes in feedback and stores the data. Also, we have a page that fetches all the the feedbacks that have been inputted and displays them. Run the flask app and enjoy.


## Conclusion
If you are first-timer this is one of the heavier concepts that we've talked about so far. This is partly because we have learned a new concept called databases and also how to interact with them. If you haven't understood this, that's okay. It takes time to understand these concepts and how they interact. Go through the code. Read through [this chapter]
(https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iv-database) on Flask mega tutorial. And most importantly

> Google is your best-est friend.

If there is something you don't understand, Google it. There are tons of content available that are much better than these notes I cooked up in the last couple of hours.

But on the off-chance that you actually understood, congratulations. You have taken the first steps in backend development. No, seriously. This is pretty much the core features of web development. You know how to route URLs to view functions, you know how to render templates with data created on the go. You know how to recieve data from forms. And now you know how to store and retrieve those data from databases. Take your favourite website and see if you can imagine their functionalities in terms of these concepts. Chances are, you can.


![You're an avenger](https://s18670.pcdn.co/wp-content/uploads/kid.gif)

## Where to next ?
- Practice, practice, practice (Do more projects with these concepts)
- It's certainly a good idea to try out more complex databases and complex queries. This is where you'll spend a lot of time.
  - Do projects with multiple tables and queries that require combining data from multiple tables.
- Deployment (we'll hopefully cover Heroku in our sessions)
- Learning how to structure large projects
- ???? (what else people ?)


## Resources
- [Flask Mega Tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world)
- [Flask Tutorial - Corey Schafer](https://www.youtube.com/watch?v=MwZwr5Tvyxo&list=PL-osiE80TeTs4UjLw5MM6OjgkjFeUxCYH)
- Will add more

> Written with [StackEdit](https://stackedit.io/).

