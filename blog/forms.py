from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.fields.core import IntegerField
from wtforms.fields.simple import FileField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from blog.model import User

class RegistrationForm(FlaskForm):
    username = StringField('',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('',
                        validators=[DataRequired(), Email()])
    password = PasswordField('', validators=[DataRequired()])
    confirm_password = PasswordField('',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('')


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
                           validators=[DataRequired(), Length(min=4, max=10)])
    money = IntegerField('',validators=[DataRequired()])
    tele =  StringField('',
                           validators=[DataRequired()])
    image        = FileField('', )
    location = StringField('',
                           validators=[DataRequired(), Length(min=4, max=10)])
    description  = TextAreaField('')