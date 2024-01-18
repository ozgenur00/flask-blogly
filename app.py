"""Blogly application."""

from flask import Flask, render_template, url_for, redirect, request
from models import db, connect_db, User, Post

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///users_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "this-is-my-secret-key:)"

connect_db(app)
db.create_all()

@app.route('/')
def base():
    return redirect('/users')

@app.route('/users')
def users_index():
    """Show a page with info on all users"""
    users = User.query.order_by(User.firstname, User.lastname).all()
    return render_template('index.html', users=users)


@app.route('/users/<int:user_id>')
def user_detail(user_id):
    """Show user detail"""
    user = User.query.get_or_404(user_id)
    return render_template('user-detail.html', user=user)

@app.route('/users/new', methods=["GET"])
def add_user_page():
    """Go to add new user page"""
    return render_template('newuser.html')


@app.route('/users/new', methods=['POST'])
def adding_user():
    firstname = request.form['firstname']
    lastname = request.form['lastname']
    image_url = request.form['image_url']
    new_user = User(firstname=firstname, lastname=lastname, image_url=image_url)
    db.session.add(new_user)
    db.session.commit()

    return redirect(f"/users")


@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect('/users')

@app.route('/users/<int:user_id>/edit')
def users_edit(user_id):
    """Show the editing form"""
    user = User.query.get_or_404(user_id)
    return render_template('edit.html', user=user)


@app.route('/users/<int:user_id>/edit/edited', methods=['POST'])
def edited_user(user_id):
    user = User.query.get_or_404(user_id)
    user.firstname = request.form['firstname']
    user.lastname = request.form['lastname']
    user.image_url = request.form['image_url'] or None

    db.session.add(user)
    db.session.commit()
    return redirect(f"/users/{user_id}")

######################POSTS###########################

@app.route('/users/posts/<int:post_id>')
def post_detail(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post_detail.html', post=post)

@app.route('/users/<int:user_id>/posts/new', methods=['GET', 'POST'])
def add_post(user_id):
    user = User.query.get_or_404(user_id)

    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        if not title or not description:
            return redirect(request.url)
        new_post = Post(title=title, content=description, user_id=user_id)
        db.session.add(new_post)
        db.session.commit()
        return redirect(f"/users/{user_id}")
    
    return render_template('add_post.html', user=user)

@app.route('/posts/<int:post_id>/edit')
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    user_id = post.user_id 
    return render_template('edit_post.html', post=post, user_id=post.user_id)

@app.route('/posts/<int:post_id>/edit/edited', methods=['POST'])
def edited_post(post_id):
    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']

    db.session.add(post)
    db.session.commit()
    return redirect(f"/users/posts/{post_id}")

@app.route('/posts/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    user_id = post.user_id
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('user_detail', user_id=user_id))


