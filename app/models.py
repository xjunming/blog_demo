from datetime import datetime
from app import db,login
from flask_login import UserMixin

@login.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()


class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    avatar_img = db.Column(db.String(120), default='/static/Avatar-Boy.png',nullable=False)
    posts = db.relationship('Post',backref=db.backref('author', lazy=True))


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140), nullable=False)
    img = db.Column(db.String(120), nullable=True)
    timestamp = db.Column(db.DateTime,default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),
                            nullable=False)
    def __repr__(self):
        return '<Post %r>' % self.body