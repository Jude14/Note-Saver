from . import db 
from flask_login import UserMixin 
from sqlalchemy import func 

class Note(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone= True), default= func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) #1 to many relationship#'user.id' like 'User.id' but SQL takes it as lowercase

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(150),unique = True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    notes = db.relationship('Note')#in the relationship i don't put it as lowercase i put it normally (only in the foreign key i put it as lowercase)

