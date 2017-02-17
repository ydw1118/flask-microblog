#coding:utf8
from datetime import datetime
from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


#文章表
class Entry(db.Model):
    __tablename__ = 'entrys'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    description = db.Column(db.String(512))
    content = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.now())
    def __repr__(self):
        return '<Title {}>'.format(self.title)


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(48))
    email = db.Column(db.String(128), unique=True)
    password_hash = db.Column(db.String(256))
    register_at = db.Column(db.DateTime, default=datetime.now())


    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verity_password(self, password):
        return check_password_hash(self.password_hash, password)
































