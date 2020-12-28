from run import db
from datetime import datetime


class Follow(db.Model):
    __tablename__ = 'follows'
    follower_id = db.Column(db.Integer, db.ForeignKey('user.id'),primary_key=True)
    followed_id = db.Column(db.Integer, db.ForeignKey('user.id'),primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def filter_by(self, followed_id, follower_id):
        pass


class User(db.Model):
    __tablename__ = 'user'
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(50),unique=True,nullable=False)
    name=db.Column(db.String(50),nullable=False)
    surname=db.Column(db.String(50),nullable=False)
    password=db.Column(db.String(50),nullable=False)
    nationality=db.Column(db.String(200),nullable=False)
    eventscreated=db.relationship('SocialEatingEvents', backref='user')
    mealsshared=db.relationship('SharedMeals', backref='user')
    eventsjoined=db.relationship('SocialEatingEvents', backref='events')
    mealspurchased=db.relationship('SharedMeals', backref='meals')
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


class SocialEatingEvents(db.Model):
    __tablename__ = 'see'
    id=db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String, nullable=False)
    date=db.Column(db.DateTime, nullable=False)
    location=db.Column(db.String, nullable=False)
    numpeople=db.Column(db.Integer, nullable=False)
    info=db.Column(db.String, nullable=False)
    creator = db.Column(db.Integer, db.ForeignKey('user.id'))
    partecipants=db.relationship('Users', backref='partecipants')
    expired=db.Column(db.Boolean, nullable=False, default=False)

#class partecipantlist
  # idevento
   # user


class SharedMeals(db.Model):
    __tablename__ = 'mealsshared'
    id = db.Column(db.Integer, primary_key=True)
    title= db.Column(db.String, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.String, nullable=False)
    info = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    expired=db.Column(db.Boolean, nullable=False, default=False)
    buyer=db.relationship('Users', backref='buyer')


class Chat(db.Model):
    __tablename__ = 'chat'
    id = db.Column(db.Integer, primary_key=True)





