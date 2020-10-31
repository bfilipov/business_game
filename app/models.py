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
    display_name = db.Column(db.String(120), unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(120))
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    member1 = db.Column(db.String(120))
    member2 = db.Column(db.String(120))
    member3 = db.Column(db.String(120))
    member4 = db.Column(db.String(120))
    member5 = db.Column(db.String(120))
    member6 = db.Column(db.String(120))
    member7 = db.Column(db.String(120))
    member8 = db.Column(db.String(120))
    member9 = db.Column(db.String(120))
    member10 = db.Column(db.String(120))

    # game specifics
    periods = db.relationship('Period', backref='player', lazy='dynamic')
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'))
    money_total = db.Column(db.Integer)

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
    demand_scenario_id = db.Column(db.Integer)

    def __repr__(self):
        return f'<Game {self.id}>'


class Userinput(db.Model):
    id = db.Column(db.String(64), primary_key=True)
    # id is in formate -> str:
    # 'game_id'_'user_id'_'period_number_product_id'

    # period reference
    period_id = db.relationship('Period', backref='userinput', lazy='dynamic')

    # product reference
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))  # A,B,C

    produce_quantity = db.Column(db.Integer)  # production
    sell_price = db.Column(db.Integer)  # price
    marketing_costs = db.Column(db.Integer)  # marketing budget
    research_and_development_costs = db.Column(db.Integer)  # R & D

    marketing_research_price = db.Column(db.Boolean)  # проучване на цени
    marketing_research_sales = db.Column(db.Boolean)  # проучване на продажби
    marketing_research_quality = db.Column(db.Boolean)  # проучване на качество
    marketing_research_marketing_costs = db.Column(db.Boolean)  # проучване на разходи за маркетинг

    approved_by_admin = db.Column(db.Boolean, default=False)


class Period(db.Model):
    id = db.Column(db.String(64), primary_key=True)
    # id is in formate -> str:
    # 'game_id'_'user_id'_'period_number'_'product'
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    period_number = db.Column(db.Integer)

    # USER INPUIT
    userinput_id = db.Column(db.String(64), db.ForeignKey('userinput.id'))

    # product reference
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))  # A,B,C

    # Приходи
    income_from_sells = db.Column(db.Integer)

    # COSTS:
    # production costs
    labot_costs = db.Column(db.Integer)  # Труд
    material_costs = db.Column(db.Integer)  # матeриали

    gross_proffit = db.Column(db.Integer)  # Брутна печалба

    # non-production costs
    marketing_costs = db.Column(db.Integer)  # маркетинг
    research_and_development_costs = db.Column(db.Integer)  # R & D
    transport_costs = db.Column(db.Integer)  # транспорт
    storage_costs = db.Column(db.Integer)  # складови
    administrative_costs = db.Column(db.Integer)  # административни
    marketing_research_costs = db.Column(db.Integer)  # разходи за проучвания
    interest_costs = db.Column(db.Integer)  # лихви (разхвърляни пропорционално)
    other_costs = db.Column(db.Integer)  # други (от сценария)

    # QUANTITY
    products_sold = db.Column(db.Integer)
    products_in_stock_beggining_of_period = db.Column(db.Integer)
    products_in_stock_end_of_period = db.Column(db.Integer)

    def __repr__(self):
        return f'<Period {self.id}>'


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)


class Scenario(db.Model):
    # Scenario per period
    id = db.Column(db.Integer, primary_key=True)
    demand_scenario_id = db.Column(db.Integer)

    period = db.Column(db.Integer)  # number of period

    # product reference
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))  # A,B,C

    demand_quantity = db.Column(db.Integer)  # брой продажби
    sensitivity_price = db.Column(db.Float)  # чувствителност цена
    sensitivity_quality = db.Column(db.Float)  # чувствителност качество
    sensitivity_marketing = db.Column(db.Float)  # чувствителност маркетинг
    correction_cost_labor = db.Column(db.Float)  # корекция на разходи за труд
    correction_cost_materials_for_one_product = db.Column(db.Float)  # корекция на разходи за материали
    cost_unpredicted = db.Column(db.Integer)  # непредвидени разходи prod
    cost_materials_for_one_product = db.Column(db.Float)  # разх. за матер. за 1 прод.
    cost_labor = db.Column(db.Float)  # разходи за труд
    investment_for_one_marketing = db.Column(db.Integer)  # единица маркетинг
    investment_for_one_quality = db.Column(db.Integer)  # необх. Инвестиция за 1 ед. Качество
    quality_index_min = db.Column(db.Float)  # макс индекси
    quality_index_max = db.Column(db.Float)  # мин индекс качество
    marketing_keep_effect = db.Column(db.Float)  # запазващ се ефект индекс маркетинг
    base_value_rand_quality = db.Column(db.Float)  # базова ст-ат за Rand на качество
    cost_transport = db.Column(db.Float)  # транспортни разходи
    cost_storage = db.Column(db.Float)  # складови разходи
    cost_fixed_administrative = db.Column(db.Integer)  # фиксирани административни разходи
    cost_product_manager = db.Column(db.Integer)  # продуктов мениджър
    cost_new_product_manager = db.Column(db.Integer)  # нов продуктов мениджър
    price_research = db.Column(db.Integer)  # цена на проучване
    # starting_capital = db.Column()  # начален капитал (заем)
    # max_loan = db.Column()  # макс. Размер на изтеглен заем за период
    interest_credit = db.Column(db.Float)  # лихвен процент кредит
    interest_overdraft = db.Column(db.Float)  # лихвен процент овърдрафт
    max_price = db.Column(db.Float)  # макс цена

# ## FILL IN DEMAND TABLE IN MIGRATION!!!!!
#
# # populate demand scenario:
# demands = {
#     'scenario_1': {
#         'scenario_id': 1,
#         'periods': [
#             {1: [200, 300, 400]},
#             {2: [200, 300, 400]},
#             {3: [200, 300, 400]},
#             {4: [200, 300, 400]},
#             {5: [200, 300, 400]},
#             {6: [200, 300, 400]},
#             {7: [200, 300, 400]},
#             {8: [200, 300, 400]},
#             {9: [200, 300, 400]},
#             {10: [200, 300, 400]},
#             {11: [200, 300, 400]},
#             {12: [200, 300, 400]},
#             {13: [200, 300, 400]},
#             {14: [200, 300, 400]},
#             {15: [200, 300, 400]},
#             {16: [200, 300, 400]},
#             {17: [200, 300, 400]},
#             {18: [200, 300, 400]},
#             {19: [200, 300, 400]},
#             {20: [200, 300, 400]},
#         ]
#     }
# }
#
#
# def upgrade():
#     # ### commands auto generated by Alembic - please adjust! ###
#     op.create_table('demand',
#     sa.Column('id', sa.Integer(), nullable=False),
#     sa.Column('demand_scenario_id', sa.Integer(), nullable=True),
#     sa.Column('period', sa.Integer(), nullable=True),
#     sa.Column('demand_A', sa.Integer(), nullable=True),
#     sa.Column('demand_B', sa.Integer(), nullable=True),
#     sa.Column('demand_C', sa.Integer(), nullable=True),
#     sa.PrimaryKeyConstraint('id')
#     )
#
#     # ### commands made by bogo ###
#     for dk, dv in demands.items():
#         for period in dv.get('periods'):
#             op.execute('INSERT INTO "demand" (id, demand_scenario_id, period, "demand_A", "demand_B", "demand_C") '
#                        'VALUES ({}, {}, {}, {}, {}, {});'
#                        .format('default', dv.get("scenario_id"),
#                                list(period.keys())[0], list(period.values())[0][0],
#                                list(period.values())[0][1], list(period.values())[0][2]))
#
# ## FILL IN DEMAND TABLE!!!!!
# ## FILL IN DEMAND TABLE!!!!!
# ## FILL IN DEMAND TABLE!!!!!
# ## FILL IN DEMAND TABLE!!!!!
