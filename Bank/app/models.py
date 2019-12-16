from app import db
from flask_login import UserMixin

link = db.Table('link',db.Model.metadata,
                 db.Column('account_id',db.Integer,db.ForeignKey('Account.id')),
                 db.Column('accoiunt_email',db.Integer,db.ForeignKey('Account..User.email')))

class User(UserMixin,db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(10),index=True)
    pwd = db.Column(db.String(20),index=True)
    email = db.Column(db.String(30),index=True,unique=True)
    manager = db.Column(db.Boolean,index=True)

    account = db.relationship('Account',uselist=False,backref="User")

    def __repr__(self):
        return '<User %r>' % self.name


class Account(db.Model):
    __tablename__ = 'Account'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    score = db.Column(db.Float,index=True)
    loan = db.Column(db.Float,index=True,default=0)
    money = db.Column(db.Float,index=True)
    trans = db.relationship('Account',secondary=link)
    owner_id = db.Column(db.Integer,db.ForeignKey('User.id'))

    owner = db.relationship('User')

    def __repr__(self):
        return '<Account %r' % self.code

