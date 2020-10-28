from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField, BooleanField, SubmitField
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

    produce_quantity = IntegerField('Производство', validators=[NumberRange(min=1, max=100)])  # production
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
