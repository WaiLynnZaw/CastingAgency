import os
from sqlalchemy import Column, String, Integer
from flask_sqlalchemy import SQLAlchemy
import json

# load_dotenv()
# database_name = os.getenv("DB_NAME")
# database_url = os.getenv("DB_URL")
database_path = os.environ['DATABASE_URL']
if database_path.startswith("postgres://"):
  database_path = database_path.replace("postgres://", "postgresql://", 1)

db = SQLAlchemy()

def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    app.app_context().push()
    db.init_app(app)
    db.create_all()

class Movie(db.Model):
    __tablename__ = 'movies'
    
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    release_date = Column(String, nullable=False)
    
    def __init__(self, title, release_date):
        self.title = title
        self.release_date = release_date

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date
            }
        
class Actor(db.Model):
    __tablename__ = 'actors'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    age = db.Column(Integer, nullable=False)
    gender = db.Column(String)
    
    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender
            }