"""Blogly application."""

from flask import Flask, render_template, url_for, redirect, request
from models import db, connect_db, User, Post, Tag, PostTag

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
    tags = Tag.query.all()

    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('description')
        selected_tags_ids = request.form.getlist('tags')  
        selected_tags = Tag.query.filter(Tag.id.in_(selected_tags_ids)).all() 
        
        if not title or not content:
            return redirect(request.url)
        
        new_post = Post(title=title, content=content, user_id=user_id)
        new_post.tags = selected_tags 
        db.session.add(new_post)
        db.session.commit()
        return redirect(f"/users/{user_id}")

    return render_template('add_post.html', user=user, tags=tags)
    


@app.route('/posts/<int:post_id>/edit', methods=['GET'])
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    all_tags = Tag.query.all()  # Fetch all tags
    return render_template('edit_post.html', post=post, all_tags=all_tags, user_id=post.user_id)

@app.route('/posts/<int:post_id>/edit/edited', methods=['POST'])
def edited_post(post_id):
    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']
    
    # Update tags
    selected_tags_ids = request.form.getlist('tags')  # Get list of selected tag ids
    selected_tags = Tag.query.filter(Tag.id.in_(selected_tags_ids)).all()  # Fetch the selected tag objects
    post.tags = selected_tags  # Update the post's tags
    
    db.session.commit()
    return redirect(f"/users/posts/{post_id}")


@app.route('/posts/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    user_id = post.user_id
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('user_detail', user_id=user_id))

#############tags#######################################

@app.route('/tags')
def tag_list():
    tags = Tag.query.order_by(Tag.name).all()
    return render_template('tag_list.html', tags=tags)

@app.route('/tags/<int:tag_id>')
def tag_detail(tag_id):
    """show tag detail"""
    tag = Tag.query.get_or_404(tag_id)
    return render_template('tag_detail.html', tag=tag)

@app.route('/tags/<int:tag_id>/delete', methods=['POST'])
def delete_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()
 
    return redirect('/tags')


@app.route('/tags/new', methods=['GET'])
def new_tag():
    return render_template('new_tag.html')

@app.route('/tags/new', methods=['POST'])
def adding_tag():
    name = request.form['name']
    new_tag = Tag(name=name)
    db.session.add(new_tag)
    db.session.commit()
    return redirect(f"/tags")

@app.route('/tags/<int:tag_id>/edit', methods=['GET'])
def edit_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    return render_template('edit_tag.html', tag=tag)

@app.route('/tags/<int:tag_id>/edit/edited', methods=['POST'])
def editing_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    tag.name = request.form['name']
    db.session.add(tag)
    db.session.commit()
    return redirect("/tags")
