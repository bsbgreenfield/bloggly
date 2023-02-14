from flask import Flask, request, redirect, render_template, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, User, connect_db

app = Flask(__name__)

app.config['SECRET_KEY'] = 'benji'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

toolbar = DebugToolbarExtension(app)


app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blog_db'
app.config['SQLALCHEMY_ECHO'] = True
app.app_context().push()

connect_db(app)


@app.route('/')
def homepage():
    users = User.query.all()
    return redirect('/users')

@app.route('/users')
def user_list():
    users = User.query.all()
    return render_template('user_list.html', users=users)

@app.route('/users/new')
def create_user():
    return render_template('create.html')


@app.route('/users/new', methods=['POST'])
def submit_new_user():
    first = request.form['f_name']
    last = request.form['l_name']
    image = request.form['img_url']
    username = request.form['username']
   
    new_user = User(username = username, first_name=first, last_name=last, image_url=image)
    print(new_user)
    print(new_user.id)
    db.session.add(new_user)
    db.session.commit()
    return redirect(f'/users/{new_user.id}')


@app.route('/users/<int:user_id>')
def user_detail(user_id):
    selected_user = User.query.get(user_id)
    return render_template('user_detail.html', user=selected_user) 

@app.route('/users/<int:user_id>/edit')
def edit_user_page(user_id):
    selected_user = User.query.get(user_id)
    return render_template('edit_user.html', user=selected_user)


@app.route('/users/<int:user_id>/edit', methods = ['POST'])
def submit_user_edit(user_id):
    first = request.form['f_name']
    last = request.form['l_name']
    image = request.form['img_url']
    username = request.form['username']
    selected_user = User.query.get(user_id)
    selected_user.update_user(username, first, last, image)
    db.session.add(selected_user)
    db.session.commit()
    return redirect(f'/users/{user_id}')

@app.route('/users/<int:user_id>/delete', methods = ['POST'])
def delete_user(user_id):
    User.query.filter_by(id=user_id).delete()
    db.session.commit()
    return redirect('/users')