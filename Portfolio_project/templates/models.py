from Portfolio_project import db
from flask_sqlalchemy  import SQLAlchemy
from sqlalchemy import Column, Integer, String
from flask_login import UserMixin
from sqlalchemy.sql import func
from datetime import datetime

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150))
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    notes = db.relationship('Note')
