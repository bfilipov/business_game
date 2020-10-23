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


class PeriodForm(FlaskForm):
    product_a_produced = IntegerField('Produce A', validators=[NumberRange(min=1, max=100,
                                                                           message='пробвай пак')])
    product_b_produced = IntegerField('Produce B', validators=[NumberRange(min=1, max=100)])
    product_c_produced = IntegerField('Produce C', validators=[NumberRange(min=1, max=100)])

    price_product_a = IntegerField('Price A', validators=[NumberRange(min=1, max=100)])
    price_product_b = IntegerField('Price B', validators=[NumberRange(min=1, max=100)])
    price_product_c = IntegerField('Price C', validators=[NumberRange(min=1, max=100)])

    submit = SubmitField('Submit')


class ReviewPeriodForm(PeriodForm):
    approved = BooleanField('Approved', validators=[])
