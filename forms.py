from flask_wtf import FlaskForm
from wtforms import BooleanField, EmailField, HiddenField,  IntegerRangeField, StringField, PasswordField, SubmitField, FloatField, TextAreaField, IntegerField, DateField, TimeField
from wtforms.validators import DataRequired, Optional, NumberRange, Length
from flask_wtf.file import FileField, FileAllowed

# class LoginForm(FlaskForm):
#     username=StringField("Username", validators=[DataRequired()])
#     password=PasswordField("Password", validators=[DataRequired()])
#     submit = SubmitField("Login")

# class RegisterForm(FlaskForm):
#     username=StringField("Username", validators=[DataRequired()])
#     password=PasswordField("Password", validators=[DataRequired()])
#     email=StringField("Email", validators=[DataRequired()])
#     submit = SubmitField("Register")

# class ContactForm(FlaskForm):
#     username= StringField("Username", validators=[DataRequired()])
#     email= StringField("Email", validators=[DataRequired()])
#     message= StringField("Message", validators=[DataRequired()])
#     submit = SubmitField("Submit")


# # Форма для додавання туру
# class AddTourForm(FlaskForm):
#     name = StringField('Tour Name', validators=[DataRequired(), Length(min=2, max=100)])
#     description = TextAreaField('Description', validators=[DataRequired(), Length(min=10)])
#     price = FloatField('Price', validators=[DataRequired(), NumberRange(min=0)])
#     image = FileField('Tour Image', validators=[Optional(), FileAllowed(['jpg', 'png'], 'Images only!')])
#     submit = SubmitField('Add Tour')

# class LikeForm(FlaskForm):
#     submit = SubmitField('❤')

class CarForm(FlaskForm):
    car = StringField("Машина", validators=[DataRequired()])
    brand = StringField("Марка авто", validators=[DataRequired()])
    price = FloatField("Ціна", validators=[DataRequired()])
    body = StringField("Кузов", validators=[DataRequired()])
    image = FileField('Фото авто', validators=[Optional(), FileAllowed(['jpg', 'png'], 'Тільки фото!')])
    submit = SubmitField("Надіслати")
    
class RegisterForm(FlaskForm):
    user_name = StringField("Ім'я", validators=[DataRequired()])
    user_password = PasswordField("Пароль", validators=[DataRequired()])
    user_email = EmailField("Пошта", validators=[DataRequired()])
    user_phone = IntegerField("Номер телефону", validators=[DataRequired()])
    submit = SubmitField("Зареєструватися")

class LoginForm(FlaskForm):
    user_email = EmailField("Пошта", validators=[DataRequired()])
    user_password = PasswordField("Пароль", validators=[DataRequired()])
    submit = SubmitField("Увійти")
    
class OrderForm(FlaskForm):
    start_date = DateField('Дата начала', format='%Y-%m-%d', validators=[DataRequired()])
    start_time = TimeField('Время начала', validators=[DataRequired()])
    stop_date = DateField('Дата окончания', format='%Y-%m-%d', validators=[DataRequired()])
    stop_time = TimeField('Время окончания', validators=[DataRequired()])
    total_price = HiddenField('Итого')  # Скрытое поле для общей цены
    user_phone = IntegerField("Номер телефону", validators=[DataRequired()])
    submit = SubmitField('Создать заказ')