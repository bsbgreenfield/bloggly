from flask_sqlalchemy import SQLAlchemy


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
    
    