from flask import Flask
from models import db, Tag, Category
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
db.init_app(app)


def create_categories():
    category1 = Category(name='Разработка')
    category2 = Category(name='Прочее')
    category3 = Category(name='Новости')

    db.session.add(category1)
    db.session.add(category2)
    db.session.add(category3)
    db.session.commit()
    print('Categories added.')


def create_tags():
    tag1 = Tag(name='Flask')
    tag2 = Tag(name='Python')
    tag3 = Tag(name='Россия')

    db.session.add(tag1)
    db.session.add(tag2)
    db.session.add(tag3)
    db.session.commit()
    print('Tags added.')


def create_db():
    with app.app_context():
        db.create_all()
        create_categories()
        create_tags()
    print('Database created.')


if __name__ == '__main__':
    create_db()
