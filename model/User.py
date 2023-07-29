from flask_sqlalchemy import SQLAlchemy

from datetime import datetime


db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'  
      # Specify the custom table name
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(191), unique=True, nullable=False)
    email = db.Column(db.String(191), unique=True, nullable=False)
    password = db.Column(db.String(191), unique=True, nullable=False)
    image = db.Column(db.String(191), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)


    def __repr__(self):
        return f'<User {self.id} {self.name} {self.email} {self.image} {self.created_at}>' 
