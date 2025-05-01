from flask import Flask
from models import db, Tag, Category, User
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
db.init_app(app)


def create_categories():
    default_categories = [
        {'name': 'Разработка'},
        {'name': 'Прочее'},
        {'name': 'Новости'}
    ]
    for category in default_categories:
        if not Category.query.filter_by(name=category['name']).first():
            new_category = Category(name=category['name'])
            db.session.add(new_category)

    try:
        db.session.commit()
        print('Categories added')
    except Exception as e:
        db.session.rollback()
        print(f'Error add categories: {str(e)}')


def create_tags():
    default_tags = [
        {'name': 'Flask'},
        {'name': 'Python'},
        {'name': 'Россия'}
    ]
    for tag in default_tags:
        if not Tag.query.filter_by(name=tag['name']).first():
            new_tag = Tag(name=tag['name'])
            db.session.add(new_tag)

    try:
        db.session.commit()
        print('Tags added')
    except Exception as e:
        db.session.rollback()
        print(f'Error add tags: {str(e)}')


def create_default_user():
    with app.app_context():
        if not User.query.filter_by(username='admin').first():
            admin = User(
                username='admin',
                email='admin@example.com',
                display_name='Admin',
                is_admin=True
            )
            admin.set_password('admin')
            db.session.add(admin)
            db.session.commit()
            print("Admin user created")


def create_db():
    with app.app_context():
        db.create_all()
        create_categories()
        create_tags()
    print('Database created.')
    create_default_user()


if __name__ == '__main__':
    create_db()
