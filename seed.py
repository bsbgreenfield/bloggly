from app import app
from models import db, User, Post, Tag, PostTag

db.drop_all()
db.create_all()

user = User(
    id = 9999,
    username = "ExampleUser",
    first_name = "Mr",
    last_name   = "example"
    )
   
post = Post(
    title = "example Post",
    content = 'Example text body',
    poster = 9999

)

tag1 = Tag(
    name = "funny"
)

tag2 = Tag(
    name = "cool"
)
db.session.add_all([user, post, tag1, tag2])
db.session.commit()