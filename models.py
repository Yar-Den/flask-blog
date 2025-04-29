from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


post_tags = db.Table(
    'post_tags',
    db.Column('post_id',
              db.Integer,
              db.ForeignKey('post.id', name='fk_post_tags_post_id'),
              primary_key=True),
    db.Column('tag_id',
              db.Integer,
              db.ForeignKey('tag.id', name='fk_post_tags_tag_id'),
              primary_key=True)
               )


class Post(db.Model):
    id = db.Column(db.Integer,
                   primary_key=True
                   )
    title = db.Column(db.String(100),
                      unique=True,
                      nullable=False
                      )
    content = db.Column(db.Text,
                        nullable=False
                        )
    date = db.Column(db.DateTime,
                     nullable=False,
                     default=datetime.now()
                     )
    category_id = db.Column(db.Integer,
                            db.ForeignKey('category.id',
                                          name='fk_post_category_id'
                                          ),
                            nullable=False
                            )
    user_id = db.Column(db.Integer,
                        db.ForeignKey('user.id',
                                      name='fk_post_user_id'
                                      ),
                        nullable=False
                        )

    def __repr__(self):
        return f'<Post {self.title}>'


class Category(db.Model):
    id = db.Column(db.Integer,
                   primary_key=True
                   )
    name = db.Column(db.String(50),
                     unique=True,
                     nullable=False
                     )
    posts = db.relationship('Post',
                            backref='category',
                            lazy=True
                            )

    def __repr__(self):
        return f'<Category {self.name}>'


class Tag(db.Model):
    id = db.Column(db.Integer,
                   primary_key=True
                   )
    name = db.Column(db.String(25),
                     unique=True,
                     nullable=False
                     )
    posts = db.relationship('Post',
                            secondary=post_tags,
                            backref=db.backref('tags', lazy=True)
                            )

    def __repr__(self):
        return f'<Tag {self.name}>'


class User(UserMixin, db.Model):
    id = db.Column(db.Integer,
                   primary_key=True
                   )
    username = db.Column(db.String(40),
                         unique=True,
                         nullable=False
                         )
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(120),
                      unique=True,
                      nullable=False
                      )
    is_admin = db.Column(db.Boolean,
                         default=False
                         )
    posts = db.relationship('Post',
                            backref=db.backref('author', lazy=True)
                            )

    def __repr__(self):
        return f'<User {self.username}>'

    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str):
        check_password_hash(self.password_hash, password)
