from api import db

class User(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    email=db.Column(db.String(120),nullable=False)
    password=db.Column(db.String(120),nullable=False)