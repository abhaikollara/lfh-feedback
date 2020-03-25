_This might be a bit harder to follow if you haven't been in the 5-6PM batch since the contents of this follow directly from what was discussed in those sessions_


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

Whenever a user fills the feedback form, we capture the name and text and store it in a new row in the feedback table in our database. Similarly, whenever the user visits the `show_feedbacks` page, we are going to retrieve all the feedbacks stored in the database and display it one by one.

## sql-alchemy
The kind of database that I mentioned above is called SQL databases. In order to store, modify and retrieve data from these databases we use a language called SQL. We too can write SQL commands to communicate with our databases, but it can be cumbersome for the programmer to mix Python and SQL together. It can also be an error prone process. This is where `sql-alchemy` comes in. `sql-alchemy` is what is known as an object relational mapper (ORM). It acts as an interface between Python and an SQL database. Through sql-alchemy you can write Python code in terms of objects and classes that automatically get translated to database commands. Moreover, sql-alchemy also allows you change the underlying database system without having to change the Python code.




> Written with [StackEdit](https://stackedit.io/).