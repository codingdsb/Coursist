from flask_login import UserMixin
from .enums import CourseStatusEnum
from . import db
from sqlalchemy.orm import backref


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(150))
    courses = db.relationship("Course", backref="user", passive_deletes=True)

    def __repr__(self):
        return f"{self.name} ({self.email})"


class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1000))
    link = db.Column(db.UnicodeText())
    status = db.Column(db.Enum(CourseStatusEnum))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"))

    def __repr__(self):
        return f"{self.name}"


# TODO: Make changes to db by running db.create_all() in terminal
# TODO: Try if DB model code works properly