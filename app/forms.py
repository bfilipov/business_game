from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField, BooleanField, SubmitField, FloatField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, NumberRange

from app.models import User


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Sign in')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    repeat_password = PasswordField('Repeat Password',
                                    validators=[DataRequired(), EqualTo('password')])

    display_name = StringField('Display name', validators=[DataRequired()])

    member1 = StringField('Student 1', validators=[DataRequired()])
    member2 = StringField('Student 2')
    member3 = StringField('Student 3')
    member4 = StringField('Student 4')
    member5 = StringField('Student 5')
    member6 = StringField('Student 6')
    member7 = StringField('Student 7')
    member8 = StringField('Student 8')
    member9 = StringField('Student 9')
    member10 = StringField('Student 10')

    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Username is already taken.')

    def validate_display_name(self, display_name):
        user = User.query.filter_by(display_name=display_name.data).first()
        if user is not None:
            raise ValidationError('Display name is already taken.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Email is already taken.')


class UserInputForm(FlaskForm):

    produce_quantity = IntegerField('Производство', validators=[NumberRange(min=0, max=2000)])  # production
    sell_price = IntegerField('Цена', validators=[NumberRange(min=10, max=50)])  # production  # price
    marketing_costs = IntegerField('Бюджет за маркетинг', validators=[NumberRange(min=0, max=5000)])  # production  # marketing budget
    research_and_development_costs = IntegerField('R & D', validators=[NumberRange(min=0, max=5000)])  # production  # R & D

    marketing_research_price = BooleanField('Проучване на цени', validators=[])  # production  # проучване на цени
    marketing_research_sales = BooleanField('Проучване на продажби', validators=[])  # production  # проучване на продажби
    marketing_research_quality = BooleanField('Проучване на качество', validators=[])  # production  # проучване на качество
    marketing_research_marketing_costs = BooleanField('Проучване на разходи за маркетинг', validators=[])  # production  # проучване на разходи за маркетинг

    submit = SubmitField('Изпращане')


class UserInputPeriodTotal(FlaskForm):
    deposit_credit = IntegerField('Депозирай по кредит/депозит', validators=[NumberRange(min=0, max=10000)])
    deposit_overdraft = IntegerField('Депозирай по овердрафт', validators=[NumberRange(min=0, max=10000)])
    take_credit = IntegerField('Изтегли нов кредит', validators=[NumberRange(min=0, max=30000)])

    submit = SubmitField('Изпращане')


class ReviewUserInputPeriodTotal(UserInputPeriodTotal):
    input_approved_by_admin = BooleanField('Approved')
    submit = SubmitField('Изпращане')


class ReviewUserInputForm(UserInputForm):
    approved_by_admin = BooleanField('Approved', validators=[])
    submit = SubmitField('Submit')


class ScenarioPerPeriodForm(FlaskForm):

    demand_quantity = IntegerField('брой продажби', validators=[])  # брой продажби
    sensitivity_price = FloatField('чувствителност цена', validators=[])  # чувствителност цена
    sensitivity_quality = FloatField('чувствителност качество', validators=[])  # чувствителност качество
    sensitivity_marketing = FloatField('чувствителност маркетинг', validators=[])  # чувствителност маркетинг

    correction_cost_labor = FloatField('корекция на разходи за труд', validators=[])  # корекция на разходи за труд
    correction_cost_materials_for_one_product = FloatField('корекция на разходи за материали', validators=[])  # корекция на разходи за материали

    cost_unpredicted = IntegerField('непредвидени разходи prod', validators=[])  # непредвидени разходи prod
    cost_materials_for_one_product = FloatField('разх. за матер. за 1 прод.', validators=[])  # разх. за матер. за 1 прод.
    cost_labor = FloatField('разходи за труд', validators=[])  # разходи за труд

    investment_for_one_marketing = IntegerField('единица маркетинг', validators=[])  # единица маркетинг
    investment_for_one_quality = IntegerField('# необх. Инвестиция за 1 ед. Качество', validators=[])  # необх. Инвестиция за 1 ед. Качество

    quality_index_min = FloatField('мин индекс качество', validators=[])  # макс индекси качество
    quality_index_max = FloatField('макс индекс качество', validators=[])  # мин индекс качество

    marketing_index_min = FloatField('мин индекс маркетинг', validators=[])  # макс индекси
    marketing_index_max = FloatField('макс индекс маркетинг', validators=[])  # мин индекс качество

    marketing_keep_effect = FloatField('запазващ се ефект индекс маркетинг', validators=[])  # запазващ се ефект индекс маркетинг
    base_value_rand_quality = FloatField('# базова ст-ат за Rand на качество', validators=[])  # базова ст-ат за Rand на качество

    cost_transport = FloatField('транспортни разходи', validators=[])  # транспортни разходи
    cost_storage = FloatField('складови разходи', validators=[])  # складови разходи
    cost_fixed_administrative = IntegerField('фиксирани административни разходи', validators=[])  # фиксирани административни разходи
    cost_product_manager = IntegerField('продуктов мениджър', validators=[])  # продуктов мениджър
    cost_new_product_manager = IntegerField('нов продуктов мениджър', validators=[])  # нов продуктов мениджър

    price_research = IntegerField('цена на проучване', validators=[])  # цена на проучване
    # starting_capital = db.Column()  # начален капитал (заем)
    # max_loan = db.Column()  # макс. Размер на изтеглен заем за период
    interest_credit = FloatField('лихвен процент кредит', validators=[])  # лихвен процент кредит
    interest_overdraft = FloatField('лихвен процент овърдрафт', validators=[])  # лихвен процент овърдрафт
    max_price = FloatField('макс цена', validators=[])  # макс цена

    submit = SubmitField('Submit')


class ScenarioPerProductForm(FlaskForm):
    cost_fixed_administrative = FloatField('фиксирани административни разходи', validators=[])  # фиксирани административни разходи
    interest_credit = FloatField('лихвен процент кредит (десетична дроб)', validators=[])  # лихвен процент кредит
    interest_overdraft = FloatField('лихвен процент овърдрафт (десетична дроб)', validators=[])  # лихвен процент овърдрафт
    submit = SubmitField('Submit')


class ReviewPeriodForm(FlaskForm):
    sell_price = FloatField('sell_price', validators=[])
    income_from_sells = FloatField('income_from_sells', validators=[])
    gross_proffit = FloatField('gross_proffit', validators=[])  # Брутна печалба
    net_proffit = FloatField('net_proffit', validators=[])  # Нетна печалба
    accumulated_proffit = FloatField('accumulated_proffit', validators=[])  # натрупана печалба до момента
    labor_costs = FloatField('labor_costs', validators=[])  # Труд
    material_costs = FloatField('material_costs', validators=[])  # матeриали
    total_production_cost = FloatField('total_production_cost', validators=[])  # матeриали
    marketing_costs = FloatField('marketing_costs', validators=[])  # маркетинг // marketing budget
    research_and_development_costs = FloatField('research_and_development_costs', validators=[])  # R & D
    transport_costs = FloatField('transport_costs', validators=[])  # транспорт
    storage_costs = FloatField('storage_costs', validators=[])  # складови
    administrative_costs = FloatField('administrative_costs', validators=[])  # административни
    marketing_research_costs = FloatField('разходи за проучвания', validators=[])  # разходи за проучвания
    interest_costs = FloatField('лихви разхвърляни пропорционално', validators=[])  # лихви (разхвърляни пропорционално)
    other_costs = FloatField('други (от сценария)', validators=[])  # други (от сценария)
    total_non_production_costs = FloatField('total_non_production_costs', validators=[])  # общо
    # products_sold = IntegerField('products_sold', validators=[])
    products_in_stock_beginning_of_period = IntegerField('останали на склад в началото на периода',
                                                         validators=[])  # останали на склад в началото на периода
    products_in_stock_end_of_period = IntegerField('останали на склад след края на периода',
                                                   validators=[])  # останали на склад след края на периода
    research_price = IntegerField('research_price', validators=[])
    research_marketing = IntegerField('research_marketing', validators=[])
    research_quality = IntegerField('research_quality', validators=[])
    research_sales = IntegerField('research_sales', validators=[])
    index_marketing = FloatField('index_marketing', validators=[])
    index_quality = FloatField('index_quality', validators=[])
    consolidated_rnd_budget = FloatField('чувствителност цена',
                                         validators=[])  # натрупан бюджет за R & D // Инвестиция в R & D - натруп
    consolidated_marketing_budget = FloatField('чувствителност цена', validators=[])  # натрупан бюджет за маркетинг
    total_costs = FloatField('пълна себестойност - (произвпдствени + непроизводствени)',
                             validators=[])  # пълна себестойност - (произвпдствени + непроизводствени)
    total_costs_per_one = FloatField('пълна себестойност за брой', validators=[])  # пълна себестойност за брой
    product_manager_costs = FloatField('# разходи за продуктов мениджър за период/продукт',
                                       validators=[])  # разходи за продуктов мениджър за период/продукт
    is_producing = BooleanField('има ли производство', validators=[])  # има ли производство
    recalc_quality = FloatField('recalc_quality', validators=[])
    recalc_marketing = FloatField('recalc_marketing', validators=[])
    recalc_price = FloatField('recalc_price', validators=[])
    combined_score = FloatField('combined_score', validators=[])
    market_share = FloatField('market_share', validators=[])
    demand = IntegerField('demand', validators=[])
    direct_sells = IntegerField('direct_sells', validators=[])
    unsatisfied_demand = IntegerField('unsatisfied_demand', validators=[])
    secondary_sells = IntegerField('secondary_sells', validators=[])
    total_sells = IntegerField('total_sells / Продажби (идват от пазара)', validators=[])
    random_value = FloatField('random_value', validators=[])

    submit = SubmitField('Submit')


class ConfirmCurrentPeriodResultsForm(FlaskForm):
    approved = BooleanField('Approved?')
    submit = SubmitField('Submit')


class DoubleConfirmForm(FlaskForm):
    approved = BooleanField('Go back one period?')
    approved2 = BooleanField('Really?')
    submit = SubmitField('Submit')
