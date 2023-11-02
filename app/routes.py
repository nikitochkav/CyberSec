from datetime import datetime
from flask import render_template, flash, redirect, url_for
from app import app, db
from app.forms import ContactForm, LoginForm, RegistrationForm
from app.models import User
from flask_login import current_user, login_user, logout_user, login_required
from flask_mail import Mail, Message
from app.forms import LoginForm, RegistrationForm, ContactForm

mail = Mail(app)

current_year = datetime.now().year
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        # Отправка почты
        print(app.config['MAIL_USERNAME'])
        msg = Message('Обратная связь - CyberSec', sender=app.config['MAIL_USERNAME'], recipients=[form.email.data])
        msg.body = f'Имя: {form.name.data}\nEmail: {form.email.data}\nСообщение: {form.message.data}'
        mail.send(msg)

        flash('Ваше сообщение отправлено успешно!', 'info')
        return redirect(url_for('contact'))
    return render_template('contact.html', title='Contact Us', form=form, current_year=current_year)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Неправильный email или пароль')
            return redirect(url_for('login'))
        login_user(user)
        flash('Успешный вход!')
        return redirect(url_for('index'))
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Регистрация успешна!')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/user_dashboard')
@login_required
def user_dashboard():
    # Логика для отображения личного кабинета пользователя
    return render_template('user_dashboard.html')


from datetime import datetime

@app.context_processor
def inject_current_year():
    return {'current_year': datetime.now().year}


# # Функция для загрузки пользователя по ID
# @login_manager.user_loader
# def load_user(user_id):
#     return User.query.get(int(user_id))