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
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    repeat_password = PasswordField('Repeat Password',
                                    validators=[DataRequired(), EqualTo('password')])

    display_name = StringField('Display name', validators=[DataRequired()])

    member1 = StringField('Member 1', validators=[DataRequired()])
    member2 = StringField('Member 2')
    member3 = StringField('Member 3')
    member4 = StringField('Member 4')
    member5 = StringField('Member 5')
    member6 = StringField('Member 6')
    member7 = StringField('Member 7')
    member8 = StringField('Member 8')
    member9 = StringField('Member 9')
    member10 = StringField('Member 10')

    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Username is already taken.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Email is already taken.')


# class PeriodForm(FlaskForm):
#     product_a_produced = IntegerField(
#         'Produce A', validators=[NumberRange(min=1, max=100, message='пробвай пак')])
#     product_b_produced = IntegerField('Produce B', validators=[NumberRange(min=1, max=100)])
#     product_c_produced = IntegerField('Produce C', validators=[NumberRange(min=1, max=100)])
#
#     price_product_a = IntegerField('Price A', validators=[NumberRange(min=1, max=100)])
#     price_product_b = IntegerField('Price B', validators=[NumberRange(min=1, max=100)])
#     price_product_c = IntegerField('Price C', validators=[NumberRange(min=1, max=100)])
#
#     product_a_marketing = IntegerField('Marketing A', validators=[NumberRange(min=1, max=100)])
#     product_b_marketing = IntegerField('Marketing B', validators=[NumberRange(min=1, max=100)])
#     product_c_marketing = IntegerField('Marketing C', validators=[NumberRange(min=1, max=100)])
#
#     product_a_quality_investment = IntegerField('Quality A investment', validators=[NumberRange(min=1, max=100)])
#     product_b_quality_investment = IntegerField('Quality B investment', validators=[NumberRange(min=1, max=100)])
#     product_c_quality_investment = IntegerField('Quality C investment', validators=[NumberRange(min=1, max=100)])
#
#     submit = SubmitField('Submit')

class UserInputForm(FlaskForm):

    produce_quantity = IntegerField('Производство', validators=[NumberRange(min=0, max=10000)])  # production
    sell_price = IntegerField('Цена', validators=[NumberRange(min=1, max=100)])  # production  # price
    marketing_costs = IntegerField('Бюджет за маркетинг', validators=[NumberRange(min=1, max=100)])  # production  # marketing budget
    research_and_development_costs = IntegerField('R & D', validators=[NumberRange(min=1, max=100)])  # production  # R & D

    marketing_research_price = BooleanField('Проучване на цени', validators=[])  # production  # проучване на цени
    marketing_research_sales = BooleanField('Проучване на продажби', validators=[])  # production  # проучване на продажби
    marketing_research_quality = BooleanField('Проучване на качество', validators=[])  # production  # проучване на качество
    marketing_research_marketing_costs = BooleanField('Проучване на разходи за маркетинг', validators=[])  # production  # проучване на разходи за маркетинг

    submit = SubmitField('Submit')


class ReviewUserInputForm(UserInputForm):
    approved_by_admin = BooleanField('Approved', validators=[])


class ScenarioForm(FlaskForm):

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
