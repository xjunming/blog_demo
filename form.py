from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import StringField,PasswordField,SubmitField,BooleanField,TextAreaField
from wtforms.validators import DataRequired,Length,Email,EqualTo,ValidationError
from app.models import User

class RegisterForm(FlaskForm):
    username = StringField('用户名',validators=[DataRequired(),Length(min=3,max=20)])
    email = StringField('邮件',validators=[DataRequired(),Email()])
    password = PasswordField('密码', validators=[DataRequired(), Length(min=3, max=20)])
    confim = PasswordField('重复密码',validators=[DataRequired(),EqualTo('password')])
    # EmailConfirm = BooleanField('邮箱确认')
    # recaptcha = RecaptchaField()
    submit = SubmitField('注册')

    # 查找用户名是否已存在
    def validate_username(self,username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('用户名已被使用')

    # 查找邮件是否已存在
    def validate_email(self,email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('邮件已被使用')

class LoginForm(FlaskForm):
    username = StringField('用户名',validators=[DataRequired(),Length(min=3,max=20)])
    password = PasswordField('密码', validators=[DataRequired(), Length(min=3, max=20)])
    remember = BooleanField('记住密码')
    submit = SubmitField('登入')


class PostTweetForm(FlaskForm):
    text = TextAreaField('说些什么吧 ...',validators=[DataRequired(),Length(min=1,max=140)])
    img = FileField('选择图片',validators=[FileRequired()])
    submit = SubmitField('发送')
