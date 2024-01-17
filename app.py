"""Blogly application."""

from flask import Flask, render_template, redirect, request
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///users_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

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