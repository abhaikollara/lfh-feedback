from app import db

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=False, unique=True)
    text = db.Column(db.String(1000), index=False, unique=True)

    def __repr__(self):
        return '<Feedback {}>'.format(self.name)