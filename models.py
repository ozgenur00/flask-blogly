"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

DEFAULT_IMAGE_URL = "https://www.freeiconspng.com/uploads/icon-user-blue-symbol-people-person-generic--public-domain--21.png"

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# ... [rest of your code, including the User class] ...

def connect_db(app):
    """Connect this database to provided Flask app."""
    db.app = app
    db.init_app(app)

class User(db.Model):
    """Site user."""

    __tablename__ = "users"

    def __repr__(self):
        u = self
        return f"<User id={u.id} firstname={u.firstname} lastname={u.lastname}>"
    
    @property
    def full_name(self):
        return f"{self.firstname} {self.lastname}"


    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.Text, nullable=False)
    lastname = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.Text, nullable=False, default=DEFAULT_IMAGE_URL)