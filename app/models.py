from datetime import datetime
from hashlib import md5

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db
from app import login


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    is_admin = db.Column(db.Boolean, default=False)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(120))
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    # game specifics
    periods = db.relationship('Period', backref='player', lazy='dynamic')
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'))

    def __repr__(self):
        return f'<User {self.username}>'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @login.user_loader
    def load_user(id):
        return User.query.get(int(id))

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f'<User {self.body}>'


class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    current_period = db.Column(db.Integer, default=1)
    is_active = db.Column(db.Boolean, default=True)
    players = db.relationship('User', backref='player', lazy='dynamic')
    demand = db.relationship('Demand', backref='game', lazy='dynamic')

    def __repr__(self):
        return f'<Game {self.id}>'


class Period(db.Model):
    id = db.Column(db.String(64), primary_key=True)
    # id is in formate -> str:
    # 'game_id'_'user_id'_'period_number'

    game_id = db.Column(db.Integer, db.ForeignKey('game.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    period_number = db.Column(db.Integer)

    approved = db.Column(db.Boolean, default=False)

    price_product_a = db.Column(db.Numeric)
    price_product_b = db.Column(db.Numeric)
    price_product_c = db.Column(db.Numeric)

    in_stock_product_a = db.Column(db.Integer)
    in_stock_product_b = db.Column(db.Integer)
    in_stock_product_c = db.Column(db.Integer)

    product_a_produced = db.Column(db.Integer)
    product_b_produced = db.Column(db.Integer)
    product_c_produced = db.Column(db.Integer)

    product_a_sold = db.Column(db.Integer)
    product_b_sold = db.Column(db.Integer)
    product_c_sold = db.Column(db.Integer)

    def __repr__(self):
        return f'<Period {self.period_number}>'


class Demand(db.Model):
    # Demand per period
    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'))
    period = db.Column(db.Integer)
    demand_A = db.Column(db.Integer)
    demand_B = db.Column(db.Integer)
    demand_C = db.Column(db.Integer)
