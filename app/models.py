import os
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta

database_uri = os.getenv('DATABASE_URI')

db = SQLAlchemy()


def setup_db(app, database_path=database_uri):
    """Binds a flask application and a SQLAlchemy service"""
    app.config['SQLALCHEMY_DATABASE_URI'] = database_path
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)
    db.create_all()


class BaseModel(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Actor(BaseModel):
    __tablename__ = 'actors'

    name = db.Column(db.String(250), nullable=False)
    dob = db.Column(db.Date, nullable=False)
    gender = db.Column(db.String(250), nullable=False)

    def __init__(self, name, dob, gender):
        self.name = name
        self.dob = dob
        self.gender = gender

    def get_age(self):
        today = datetime.now().date()
        days_in_year = 365.2425
        age = (today - self.dob) // timedelta(days=days_in_year)
        return age

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.get_age(),
            'gender': self.gender,
        }


class Movie(BaseModel):
    __tablename__ = 'movies'

    title = db.Column(db.String(250), nullable=False)
    release_date = db.Column(db.Date, nullable=False)

    def __init__(self, title, release_date):
        self.title = title
        self.release_date = release_date

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            "release_date": self.release_date.strftime("%Y-%m-%d"),
        }
