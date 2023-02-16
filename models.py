from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)


class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    username = db.Column(db.String(20), nullable = False, unique = True)
    first_name = db.Column(db.String(10), nullable = False)
    last_name = db.Column(db.String(15), nullable = False)
    image_url = db.Column(db.String)
    
    def update_user(self, username, f_name, l_name, img_url):
        self.username = username
        self.first_name = f_name
        self.last_name = l_name
        self.image_url = img_url
    
    
class Post(db.Model):

    __tablename__ = "posts"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    title = db.Column(db.String(35), nullable = False, unique = True)
    content = db.Column(db.String, nullable = False)
    created_at = db.Column(db.DateTime, default = datetime.utcnow())
    poster = db.Column(db.Integer, db.ForeignKey('users.id'))

    def update_post(self, title, content):
        self.title = title
        self.content = content

    posting_user = db.relationship('User', backref = 'posts')
    post_tags = db.relationship('Tag', secondary= 'posts_tags', backref= 'posts')


class Tag(db.Model):

    __tablename__ = "tags"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    name = db.Column(db.Text, unique = True, nullable = False)

    tagged_post = db.relationship('Post', secondary='posts_tags', backref= 'tags')


class PostTag(db.Model):

    __tablename__ = 'posts_tags'

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key = True)

    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key = True)

