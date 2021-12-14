import requests

from models import db, User, Category, Post
from app import app
import uuid
import datetime


categories = [
    {'name': 'Bass', 'hashtag': '#bass',
     'description': 'Bass Players to Know, bass gear, tips,'
                    ' tutorials and tricks of the trade'},
    {'name': 'Skateboarding', 'hashtag': '#skateboarding',
     'description': 'Skateboarding in Ireland and different spots and parks'}
]

users = [
    {"first_name": "Alan", "last_name": "Anderson"},
    {"first_name": "Brian", "last_name": "Browne"},
    {"first_name": "Charlie", "last_name": "Cronin"},
]


with app.app_context():
    cats = db.session.query(Category).all()

    for cat in categories:
        try:
            new_user = Category(**cat)
            db.session.add(new_user)
            db.session.commit()
        except Exception as e:
            print(f"{e}")
            pass


with app.app_context():
    for user in users:
        try:
            new_user = User(**user)
            token = f"{uuid.uuid4()}"
            new_user.token = token

            db.session.add(new_user)
            db.session.commit()
        except Exception as e:
            print(f"{e}")
            pass



