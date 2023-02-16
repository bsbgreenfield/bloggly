from flask import Flask, request, redirect, render_template, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, User, Post, Tag, PostTag, connect_db
from forms import AddTagForm

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

    new_user = User(username=username, first_name=first,
                    last_name=last, image_url=image)
    print(new_user)
    print(new_user.id)
    db.session.add(new_user)
    db.session.commit()
    return redirect(f'/users/{new_user.id}')


@app.route('/users/<int:user_id>')
def user_detail(user_id):
    selected_user = User.query.get(user_id)
    posts = Post.query.filter(Post.poster == user_id)
    return render_template('user_detail.html', user=selected_user, posts=posts)


@app.route('/users/<int:user_id>/edit')
def edit_user_page(user_id):
    selected_user = User.query.get(user_id)
    return render_template('edit_user.html', user=selected_user)


@app.route('/users/<int:user_id>/edit', methods=['POST'])
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


@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    User.query.filter_by(id=user_id).delete()
    db.session.commit()
    return redirect('/users')


@app.route('/users/<int:user_id>/post')
def make_post(user_id):
    selected_user = User.query.get(user_id)
    return render_template('edit_post.html', user=selected_user)


@app.route('/users/<int:user_id>/post', methods=['POST'])
def send_post(user_id):
    title = request.form['title']
    content = request.form['content']
    new_post = Post(title=title, content=content, poster=user_id)
    db.session.add(new_post)
    db.session.commit()
    return redirect(f'/users/{user_id}')


@app.route('/posts/<int:post_id>')
def view_post(post_id):
    tagform = AddTagForm()
    tagform.tag.choices = [(tag.id, tag.name) for tag in Tag.query.all()]
    selected_post = Post.query.get_or_404(post_id)
    tags = selected_post.tags
    return render_template('posts.html', post=selected_post, tags=tags, form = tagform)


@app.route('/posts/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    selected_post = Post.query.get(post_id)
    user_id = selected_post.poster
    Post.query.filter_by(id=post_id).delete()
    db.session.commit()
    return redirect(f'/users/{user_id}')


@app.route('/posts/<int:post_id>/edit')
def edit_post_page(post_id):
    tagform = AddTagForm()
    tagform.tag.choices = [(tag.id, tag.name) for tag in Tag.query.all()]
    selected_post = Post.query.get_or_404(post_id)
    selected_user = selected_post.posting_user
    tags = selected_post.tags
    return render_template('edit_post.html', post=selected_post,
                           user=selected_user,
                           tags=tags,
                           form = tagform)


@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def submit_edited_post(post_id):
    selected_post = Post.query.get_or_404(post_id)
    user_id = selected_post.poster
    title = request.form['title']
    content = request.form['content']
    selected_post.update_post(title, content)
    db.session.add(selected_post)
    db.session.commit()
    return redirect(f'/users/{user_id}')


@app.route('/tags/list')
def view_tags():
    tags = Tag.query.all()
    return render_template('tags_list.html', tags=tags)


@app.route('/tags/add')
def view_add_tag():
    return render_template('add_tag.html')


@app.route('/tags/add', methods=['POST'])
def submit_new_tag():
    tagname = request.form['tagname']
    new_tag = Tag(name=tagname)
    db.session.add(new_tag)
    db.session.commit()
    return redirect(f'/tags/{new_tag.id}')


@app.route('/tags/<int:tag_id>')
def view_tag(tag_id):
    selected_tag = Tag.query.get(tag_id)
    return render_template('tag.html', tag=selected_tag)


@app.route('/posts/<int:post_id>/attach_tag', methods=['POST'])
def attach_tag(post_id):
    tagform = AddTagForm()
    tagform.tag.choices = [(tag.id, tag.name) for tag in Tag.query.all()]
    if tagform.validate_on_submit():
        selected_tag = Tag.query.get(tagform.tag.data)
        selected_post = Post.query.get(post_id)
        if selected_tag not in selected_post.tags:
            selected_post.tags.append(selected_tag)
            db.session.add(selected_post)
            db.session.commit()
        else:
            flash("tag already in use for this post!")
    if 'static-add-tag' in request.form:
        return redirect(f'/posts/{post_id}')
    return redirect(f'/posts/{post_id}/edit')



@app.route('/posts/<int:post_id>/remove_tag/<int:tag_id>', methods=['POST'])
def remove_tag(post_id, tag_id):
    selected_post = Post.query.get(post_id)
    tag_goner = Tag.query.get(tag_id)
    selected_post.tags.remove(tag_goner)
    db.session.add(selected_post)
    db.session.commit()
    return redirect(f'/posts/{post_id}/edit')
