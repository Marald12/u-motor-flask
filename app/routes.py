from flask import redirect, render_template, request, url_for, flash, Blueprint
from app import db
from app.models import Cars, User, Order
from forms import CarForm, RegisterForm, LoginForm, OrderForm
from config import Config
import os
from flask_login import login_required, login_remembered, login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

bp = Blueprint("main", __name__)
UPLOAD_FOLDER_CARS = Config.UPLOAD_FOLDER_CARS
UPLOAD_FOLDER_USERS = Config.UPLOAD_FOLDER_USERS

def register_or_login():
    loginForm = LoginForm()

    if loginForm.validate_on_submit():
        # Поиск пользователя по email
        user = User.query.filter_by(user_email=form.user_email.data).first()

        # Проверка пароля (желательно хранить хэш пароля вместо текста)
        if user and check_password_hash(user.user_password, form.user_password.data):
            login_user(user)
            flash("You have successfully logged in!", 'success')
            return redirect(url_for('main.home'))
        else:
            flash('Invalid email or password. Please try again.', 'danger')

    registerForm = RegisterForm()

    if registerForm.validate_on_submit():
        # Создаем нового пользователя
        hashed_password = generate_password_hash(form.user_password.data)
        new_user = User(user_name=form.user_name.data,
                        user_password=hashed_password,
                        user_phone=form.user_phone.data,
                        user_email=form.user_email.data)
        db.session.add(new_user)
        db.session.commit()

        # Логиним пользователя после регистрации
        login_user(new_user)
        flash("Registration successful! You are now logged in.", 'success')
        db.session.close()
        return redirect(url_for("main.home"))

    return [loginForm, registerForm]
    
@bp.route('/')
def home():
    forms = register_or_login()

    return render_template('home.html', loginForm=forms[0], registerForm=forms[1])

@bp.route('/add_new_car', methods=["POST", "GET"])
def add_new_car():
    form = CarForm()
    
    if form.validate_on_submit():
        file = form.image.data
        if file:
            filestorage = os.path.join(UPLOAD_FOLDER_CARS, file.filename)
            with open(filestorage, 'wb') as f:
                f.write(file.read())
        
        new_car = Cars(car=form.car.data, brand=form.brand.data, price=form.price.data, body=form.body.data, image=file.filename)
        db.session.add(new_car)
        db.session.commit()
        return redirect(url_for('main.home'))

    return render_template("add_new_car.html", form=form)


@bp.route('/cars', methods=["GET"])
def cars():
    cars = Cars.query.all()
    forms = register_or_login()

    return render_template("cars.html", cars=cars, loginForm=forms[0], registerForm=forms[1])

@bp.route('/register', methods=["GET", "POST"])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        # Создаем нового пользователя
        hashed_password = generate_password_hash(form.user_password.data)
        new_user = User(user_name=form.user_name.data,
                        user_password=hashed_password,
                        user_phone=form.user_phone.data,
                        user_email=form.user_email.data)
        db.session.add(new_user)
        db.session.commit()

        # Логиним пользователя после регистрации
        login_user(new_user)
        flash("Registration successful! You are now logged in.", 'success')
        db.session.close()
        return redirect(url_for("main.home"))

    # Если это GET-запрос или форма не прошла валидацию, вернем шаблон
    return render_template('register.html', form=form)

@bp.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        # Поиск пользователя по email
        user = User.query.filter_by(user_email=form.user_email.data).first()

        # Проверка пароля (желательно хранить хэш пароля вместо текста)
        if user and check_password_hash(user.user_password, form.user_password.data):
            login_user(user)
            flash("You have successfully logged in!", 'success')
            return redirect(url_for('main.home'))
        else:
            flash('Invalid email or password. Please try again.', 'danger')

    # Если это GET-запрос или форма не прошла валидацию, вернем шаблон
    return render_template('login.html', form=form)

@bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You logouted!", 'success')
    return redirect(url_for("main.home"))

@bp.route("/my_profile/<string:user_name>", methods=["GET", "POST"])
@login_required 
def my_profile(user_name):
    forms = register_or_login()
    user = User.query.filter_by(user_name=user_name).first()
    if not user:
        flash('Пользователь не найден', 'warning')
        return redirect(url_for('main.home'))

    return render_template("my_profile.html", user=user, loginForm=forms[0], registerForm=forms[1])

@bp.route('/cars/create-order/<int:car_id>', methods=["GET", "POST"])
def create_order(car_id):
    form = OrderForm()
    car = Cars.query.filter_by(id=car_id).first()
    forms = register_or_login()

    
    # Проверка существования автомобиля
    if car is None:
        flash("Автомобиль не найден.", "error")
        return redirect(url_for('main.home'))
    
    if current_user.is_authenticated:
        del form.user_phone

    if form.validate_on_submit():
        print("GKAGEJOHGOJAHGJEKOAHGJEAGHJAHGLMNGEANGJKON")
        total_price = float(form.total_price.data)

        if current_user.is_authenticated:
            user_id = current_user.id
            user_phone = current_user.user_phone
        else:
            user_id = None  # Указываем, что у незарегистрированного пользователя нет ID
            user_phone = form.user_phone.data  # Используем номер телефона из формы

        # Преобразование даты в строку и времени в строку
        start_date_str = form.start_date.data.strftime('%Y-%m-%d')  # Дата в строку 'YYYY-MM-DD'
        start_time_str = form.start_time.data.strftime('%H:%M:%S')  # Время в строку 'HH:MM:SS'

        stop_date_str = form.stop_date.data.strftime('%Y-%m-%d')  # Дата в строку 'YYYY-MM-DD'
        stop_time_str = form.stop_time.data.strftime('%H:%M:%S')  # Время в строку 'HH:MM:SS'

        # Объединение даты и времени
        start_datetime_str = start_date_str + ' ' + start_time_str
        stop_datetime_str = stop_date_str + ' ' + stop_time_str

        # Преобразование строки в объект datetime
        start_date = datetime.strptime(start_datetime_str, '%Y-%m-%d %H:%M:%S')
        stop_date = datetime.strptime(stop_datetime_str, '%Y-%m-%d %H:%M:%S')

        new_order = Order(
            car_id=car_id,
            start_date=start_date,
            stop_date=stop_date,
            total_price=total_price,
            user_id=user_id,
            user_phone=user_phone
        )

        
        
        db.session.add(new_order)
        db.session.commit()
        flash("Заказ успешно создан!", "success")
        return redirect(url_for('main.home'))


    return render_template('create_order.html', form=form, car=car, loginForm=forms[0], registerForm=forms[1])

@bp.route('/edit')
def edit():
    forms = register_or_login()

    cars = Cars.query.all()  # Получаем все машины из базы данных
    return render_template("edit.html", cars=cars, loginForm=forms[0], registerForm=forms[1])

@bp.route('/edit/del<int:car_id>')
def delete(car_id):
    car = Cars.query.filter_by(id=car_id).first_or_404()

    # Обрабатываем заказы, связанные с этим автомобилем
    orders = Order.query.filter_by(car_id=car_id).all()
    for order in orders:
        # Можно либо удалить заказы, либо обновить их, назначив другой car_id
        db.session.delete(order)  # Если нужно удалить заказы

    db.session.delete(car)
    db.session.commit()
    return redirect(url_for("main.edit"))
