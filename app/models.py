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
    userinput = db.relationship('Userinput', backref='player', lazy='dynamic')

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

    # user ref
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    # period reference
    period_id = db.relationship('Period', backref='userinput', lazy='dynamic')
    period_number = db.Column(db.Integer)

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


class PeriodTotals(db.Model):
    # id format -> str:
    # 'game_id'_'user_id'_'period_number'
    id = db.Column(db.String(64), primary_key=True)

    game_id = db.Column(db.Integer, db.ForeignKey('game.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    period_number = db.Column(db.Integer)

    # used for calculations on current period
    money_total_begining_of_period = db.Column(db.Float)
    money_total_end_of_period = db.Column(db.Float)
    total_production_quantity = db.Column(db.Integer)
    total_administrative_costs = db.Column(db.Float)
    total_interest_costs = db.Column(db.Float)

    # finansial
    money_total = db.Column(db.Float)  # разполагаеми средства
    credit_total = db.Column(db.Float)  # Кредит/депозит
    overdraft = db.Column(db.Float)  # овърдрафт


class Period(db.Model):
    # id format -> str:
    # 'game_id'_'user_id'_'period_number'_'product'
    id = db.Column(db.String(64), primary_key=True)

    game_id = db.Column(db.Integer, db.ForeignKey('game.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    period_number = db.Column(db.Integer)

    # USER INPUIT
    userinput_id = db.Column(db.String(64), db.ForeignKey('userinput.id'))

    # product reference
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))  # A,B,C

    sell_price = db.Column(db.Float)

    # Income/proffit
    income_from_sells = db.Column(db.Float)
    gross_proffit = db.Column(db.Float)  # Брутна печалба
    net_proffit = db.Column(db.Float)  # Нетна печалба
    accumulated_proffit = db.Column(db.Float)  # натрупана печалба до момента

    # COSTS:
    # production costs
    labor_costs = db.Column(db.Float)  # Труд
    material_costs = db.Column(db.Float)  # матeриали
    total_production_cost = db.Column(db.Float)  # матeриали

    # non-production costs
    marketing_costs = db.Column(db.Float)  # маркетинг // marketing budget
    research_and_development_costs = db.Column(db.Float)  # R & D
    transport_costs = db.Column(db.Float)  # транспорт
    storage_costs = db.Column(db.Float)  # складови
    administrative_costs = db.Column(db.Float)  # административни
    marketing_research_costs = db.Column(db.Float)  # разходи за проучвания
    interest_costs = db.Column(db.Float)  # лихви (разхвърляни пропорционално)
    other_costs = db.Column(db.Float)  # други (от сценария)
    total_non_production_costs = db.Column(db.Float)  # общо

    # QUANTITY
    products_sold = db.Column(db.Integer)  # Продажби (идват от пазара)
    products_in_stock_beginning_of_period = db.Column(db.Integer)  # останали на склад в началото на периода
    products_in_stock_end_of_period = db.Column(db.Integer)  # останали на склад след края на периода

    # research
    research_price = db.Column(db.Integer)
    research_marketing = db.Column(db.Integer)
    research_quality = db.Column(db.Integer)
    research_sales = db.Column(db.Integer)

    # dummy variables // изчисляеми, но скрити стойности
    index_marketing = db.Column(db.Float)
    index_quality = db.Column(db.Float)

    consolidated_rnd_budget = db.Column(db.Float)  # натрупан бюджет за R & D // Инвестиция в R & D - натруп
    consolidated_marketing_budget = db.Column(db.Float)  # натрупан бюджет за маркетинг

    total_costs = db.Column(db.Float)  # пълна себестойност - (произвпдствени + непроизводствени) / брой продукция
    product_manager_costs = db.Column(db.Float)  # разходи за продуктов мениджър за период/продукт
    is_producing = db.Column(db.Boolean)  # има ли производство

    # market fields
    recalc_quality = db.Column(db.Float)
    recalc_marketing = db.Column(db.Float)
    recalc_price = db.Column(db.Float)
    combined_score = db.Column(db.Float)

    market_share = db.Column(db.Float)
    demand = db.Column(db.Integer)
    direct_sells = db.Column(db.Integer)
    unsatisfied_demand = db.Column(db.Integer)
    secondary_sells = db.Column(db.Integer)
    total_sells = db.Column(db.Integer)

    # random
    random_value = db.Column(db.Float)

    def __repr__(self):
        return f'<Period {self.id}>'


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)


class ScenarioPerPeriod(db.Model):
    # Scenario per period
    id = db.Column(db.Integer, primary_key=True)
    demand_scenario_id = db.Column(db.Integer)
    period = db.Column(db.Integer)  # number of period

    cost_fixed_administrative = db.Column(db.Integer)  # фиксирани административни разходи
    interest_credit = db.Column(db.Float)  # лихвен процент кредит
    interest_overdraft = db.Column(db.Float)  # лихвен процент овърдрафт


class ScenarioPerProduct(db.Model):
    # Scenario per product
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

    quality_index_min = db.Column(db.Float)  # макс индекс качество
    quality_index_max = db.Column(db.Float)  # мин индекс качество

    marketing_index_min = db.Column(db.Float)  # макс индекс маркетинг
    marketing_index_max = db.Column(db.Float)  # мин индекс маркетинг

    marketing_keep_effect = db.Column(db.Float)  # запазващ се ефект индекс маркетинг
    base_value_rand_quality = db.Column(db.Float)  # базова ст-ат за Rand на качество

    cost_transport = db.Column(db.Float)  # транспортни разходи
    cost_storage = db.Column(db.Float)  # складови разходи
    # cost_fixed_administrative = db.Column(db.Integer)  # фиксирани административни разходи
    cost_product_manager = db.Column(db.Integer)  # продуктов мениджър
    cost_new_product_manager = db.Column(db.Integer)  # нов продуктов мениджър

    price_research = db.Column(db.Integer)  # цена на проучване
    # starting_capital = db.Column()  # начален капитал (заем)
    # max_loan = db.Column()  # макс. Размер на изтеглен заем за период
    # interest_credit = db.Column(db.Float)  # лихвен процент кредит
    # interest_overdraft = db.Column(db.Float)  # лихвен процент овърдрафт

    max_price = db.Column(db.Float)  # макс цена

    # # custom commands
    # # add default admin
    # op.execute("INSERT INTO \"user\" (id, is_admin, username, display_name, email, password_hash) "
    #            "VALUES (default, TRUE, 'admin', 'баце Марчев', 'filipov.bogomil@gmal.com', "
    #            "'pbkdf2:sha256:150000$4cxvcwnI$dd8e2193d11aed58163e6e2fbe57283cf69cb3dd"
    #            "af24dec0b4ae8b579112bf29');")
    #
    # # populate products
    # for product in [(1, 'Кисело мляко 1'), (2, 'Кисело мляко 2'), (3, 'Кисело мляко 3')]:
    #     op.execute(f"INSERT INTO \"product\" (id, name) VALUES ({product[0]}, '{product[1]}');")
    #
    # # populate scenario per product
    # for product in [1, 2, 3]:
    #     cost_materials = product + 2
    #
    #     for period in range(1, 21):
    #         cost_unpredicted = 0
    #
    #         op.execute('INSERT INTO "scenario_per_product" (id, demand_scenario_id, period, product_id, '
    #                    'demand_quantity, sensitivity_price, sensitivity_quality, sensitivity_marketing, '
    #                    'correction_cost_labor, correction_cost_materials_for_one_product, '
    #                    'cost_unpredicted, cost_materials_for_one_product, cost_labor, investment_for_one_marketing, '
    #                    'investment_for_one_quality, quality_index_min, quality_index_max, marketing_index_min, '
    #                    'marketing_index_max, marketing_keep_effect, base_value_rand_quality, cost_transport, '
    #                    'cost_storage, cost_product_manager, cost_new_product_manager, price_research, max_price) '
    #                    f'VALUES (default, 1, {period}, {product}, 3850, 1, 1.05, 0.95, 1, 1, {cost_unpredicted}, '
    #                    f'{cost_materials}, 5, 200, 1000, 2, 5, 2, 5, 0.5, 0.7, 1.5, 0.5, 1000, 1500, 500, 50);')
    #
    # # populate scenario per period
    # for period in range(1, 21):
    #     op.execute('INSERT INTO "scenario_per_period" (id, demand_scenario_id, period, cost_fixed_administrative, '
    #                'interest_credit, interest_overdraft) '
    #                f'VALUES (default, 1, {period}, 5000, 0.05, 0.1);')
    # # ### end Alembic commands ###

