from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms import validators
from wtforms.fields.core import IntegerField
from wtforms.fields.simple import FileField, TextAreaField, TextField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from blog.model import User,Restaurant

class RegistrationForm(FlaskForm):
    username = StringField('',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('',
                        validators=[DataRequired(), Email()])
    password = PasswordField('', validators=[DataRequired()])
    confirm_password = PasswordField('',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('')
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    email = StringField('',
                        validators=[DataRequired(), Email()])
    password = PasswordField('', validators=[DataRequired()])
 
    submit = SubmitField('登入')


class ResetPasswordFormEmail(FlaskForm):
    email = StringField( validators=[DataRequired(),Email() ])
    submit  = SubmitField()
    def validate_email(self,field):
        if not User.query.filter_by(email=field.data).first():
            raise ValidationError('沒有這個信箱')


class FormResetPassword(FlaskForm):
    """使用者申請遺失密碼"""
    password = PasswordField('', validators=[DataRequired()])
    confirm_password = PasswordField('',
                                     validators=[DataRequired(), EqualTo('password')])
    
class RestuarantForm(FlaskForm):
    """餐廳資訊"""
    title = StringField('',
                           validators=[DataRequired(), Length(min=2, max=7)])
    money = IntegerField('',validators=[DataRequired()])
    tele =  StringField('',
                           validators=[DataRequired()])
    image        = FileField('',validators=[DataRequired()])
    location = StringField('',
                           [validators.AnyOf(values=['中央後門','宵夜街','校內','市區'])])
    description  = TextAreaField('',validators=[DataRequired(), Length(min=4, max=10)])
    def validate_title(self, title):
        title = Restaurant.query.filter_by(title=title.data).first()
        if title:
            raise ValidationError('有人新增過了別皮')
class PostForm(FlaskForm):
    "評論資訊"
    post = TextAreaField('',validators=[DataRequired(),Length(min=10,max=100)])
    rate = IntegerField('',validators=[DataRequired()])
