from run import db, app
from datetime import datetime
from flask_login import UserMixin, LoginManager, login_user, login_required, logout_user, current_user

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class Follow(db.Model):
    __tablename__ = 'follows'
    follower_id = db.Column(db.Integer, db.ForeignKey('users.id'),primary_key=True)
    followed_id = db.Column(db.Integer, db.ForeignKey('users.id'),primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def filter_by(self, followed_id, follower_id):
        pass


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(50),nullable=False)
    surname=db.Column(db.String(50),nullable=False)
    nationality = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password=db.Column(db.String(50),nullable=False)
    eventscreated=db.relationship('SocialEatingEvent', backref='user')
    mealsshared=db.relationship('SharedMeal', backref='user')
    eventsjoined=db.relationship('SocialEatingEvent', backref='events')
    mealspurchased=db.relationship('SharedMeal', backref='meals')
    followed = db.relationship('Follow', foreign_keys=[Follow.follower_id],backref=db.backref('follower', lazy='joined'),lazy='dynamic',cascade='all, delete-orphan')
    followers = db.relationship('Follow', foreign_keys=[Follow.followed_id],backref=db.backref('followed', lazy='joined'),lazy='dynamic',cascade='all, delete-orphan')


    def __repr__(self):
        return "<User %r>" % self.name

    def follow(self, user):
        if not self.is_following(user):
            f = Follow(follower=self, followed=user)
            db.session.add(f)

    def unfollow(self, user):
        f = self.followed.filter_by(followed_id=user.id).first()
        if f:
            db.session.delete(f)

    def is_following(self, user):
        if user.id is None:
            return False
        return self.followed.filter_by(followed_id=user.id).first() is not None

    def is_followed_by(self, user):
        if user.id is None:
            return False
        return self.followers.filter_by(follower_id=user.id).first() is not None

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

partecipants=db.Table('partecipants', db.Column('see_id', db.Integer, db.ForeignKey('see.id'), primary_key=True),
                      db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True))

class SocialEatingEvent(db.Model):
    __tablename__ = 'see'
    id=db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String, nullable=False)
    timetable = db.Column(db.String, nullable=False)
    date=db.Column(db.DateTime, nullable=False)
    price = db.Column (db.Integer, nullable=False)
    menu = db.Column(db.String, nullable=False)
    numpeople = db.Column(db.Integer, nullable=False)
    location=db.Column(db.String, nullable=False)
    description=db.Column(db.String, nullable=False)
    creator = db.Column(db.Integer, db.ForeignKey('users.id'))
    partecipants=db.relationship('User', secondary=partecipants, lazy='subquery', backref=db.backref('see', lazy=True))
    expired=db.Column(db.Boolean, nullable=False, default=False)


class SharedMeal(db.Model):
    __tablename__ = 'mealsshared'
    id = db.Column(db.Integer, primary_key=True)
    meal= db.Column(db.String, nullable=False)
    menu = db.Column(db.String, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    expired=db.Column(db.Boolean, nullable=False, default=False)
    buyer=db.relationship('User', backref='buyer')


class Chat(db.Model):
    __tablename__ = 'chat'
    id = db.Column(db.Integer, primary_key=True)





