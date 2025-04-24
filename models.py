from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


post_tags = db.Table('post_tags',
                     db.Column('post_id', db.Integer, db.ForeignKey('post.id'),
                               primary_key=True),
                     db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'),
                               primary_key=True))


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=True, nullable=False)
    content = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.now())
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'),
                            nullable=False)

    def __repr__(self):
        return f'<Post {self.name}>'


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    post = db.relationship('Post', backref='category', lazy=True)

    def __repr__(self):
        return f'<Category {self.name}>'


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), unique=True, nullable=False)
    post = db.relationship('Post', secondary=post_tags,
                           backref=db.backref('tag', lazy=True))

    def __repr__(self):
        return f'<Tag {self.name}>'
