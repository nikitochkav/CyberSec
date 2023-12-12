from datetime import datetime
from flask import (
    render_template, flash, redirect, url_for, request, jsonify
)
from flask_mail import Mail, Message
from flask_login import current_user, login_user, logout_user, login_required
from flask_jwt_extended import create_access_token
from app import app, db
from app.forms import (
    ContactForm, LoginForm, RegistrationForm,
    ForumPostForm, ForumCommentForm
)
from app.models import User, Service, Attack, ForumPost, ForumComment

mail = Mail(app)

# Главная страница
@app.route('/')
def index():
    post = ForumPost.query.first()
    return render_template('index.html')

# Страница "О компании"
@app.route('/about')
def about():
    return render_template('about.html')

# Страница контактов
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        msg = Message(
            'Обратная связь - CyberSec',
            sender=app.config['MAIL_USERNAME'],
            recipients=[form.email.data]
        )
        msg.body = f'Имя: {form.name.data}\nEmail: {form.email.data}\nСообщение: {form.message.data}'
        mail.send(msg)

        flash('Ваше сообщение отправлено успешно!', 'info')
        return redirect(url_for('contact'))
    return render_template('contact.html', title='Contact Us', form=form, current_year=datetime.now().year)

# Страница входа в систему
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('user_dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Успешный вход!')
            return redirect(url_for('user_dashboard'))
        else:
            flash('Неправильный email или пароль')
    return render_template('login.html', form=form)

# Выход из системы
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

# Страница регистрации нового пользователя
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('user_dashboard'))
    form = RegistrationForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user:
            flash('Пользователь с таким именем уже существует. Пожалуйста, выберите другое имя пользователя.', 'danger')
            return redirect(url_for('register'))

        new_user = User(username=form.username.data, email=form.email.data, role='admin' if form.admin.data else 'user')
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash('Регистрация успешна!')
        return redirect(url_for('user_dashboard'))
    return render_template('register.html', form=form)

# Личный кабинет пользователя
@app.route('/user_dashboard')
@login_required
def user_dashboard():
    user_info = current_user
    attacks_data = Attack.query.all()
    services = Service.query.all()
    return render_template('user_dashboard.html', user_info=user_info, attacks_data=attacks_data, services=services)

# Форум
@app.route('/forum', methods=['GET', 'POST'])
@login_required
def forum():
    form = ForumPostForm()
    if form.validate_on_submit():
        new_post = ForumPost(title=form.title.data, content=form.content.data, user=current_user)
        db.session.add(new_post)
        db.session.commit()
        flash('Сообщение добавлено успешно!', 'success')
        return redirect(url_for('forum'))

    search_input = request.form.get('searchInput')
    if search_input:
        posts = ForumPost.query.filter(ForumPost.content.ilike(f"%{search_input}%")).all()
    else:
        posts = ForumPost.query.all()

    return render_template('forum.html', form=form, posts=posts, is_admin=current_user.is_admin())

# Страница поста на форуме
@app.route('/forum/post/<int:post_id>', methods=['GET', 'POST'])
@login_required
def forum_post(post_id):
    post = ForumPost.query.get_or_404(post_id)
    form = ForumCommentForm()
    if form.validate_on_submit():
        new_comment = ForumComment(content=form.content.data, user=current_user, post=post)
        db.session.add(new_comment)
        db.session.commit()
        flash('Комментарий добавлен успешно!', 'success')
        return redirect(url_for('forum_post', post_id=post.id))

    return render_template('forum_post.html', post=post, form=form)

# Редактирование поста на форуме
@app.route('/forum/edit/<int:post_id>', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    post = ForumPost.query.get_or_404(post_id)
    if current_user != post.user and not current_user.is_admin():
        flash('Вы не можете редактировать этот пост.', 'danger')
        return redirect(url_for('forum'))

    form = ForumPostForm(obj=post)
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        form.populate_obj(post)
        db.session.commit()
        flash('Пост успешно отредактирован!', 'success')
        return redirect(url_for('forum_post', post_id=post.id))

    form.title.data = post.title
    form.content.data = post.content

    return render_template('edit_post.html', form=form, post=post)

# Удаление поста на форуме
@app.route('/forum/delete/<int:post_id>', methods=['GET', 'POST'])
@login_required
def delete_post(post_id):
    post = ForumPost.query.get_or_404(post_id)
    if current_user.is_admin() or current_user == post.user:
        if request.method == 'POST':
            db.session.delete(post)
            db.session.commit()
            flash('Пост успешно удален!', 'success')
            return redirect(url_for('forum'))

        return render_template('delete_post.html', post=post)
    else:
        flash('У вас нет прав для удаления этого поста', 'danger')
        return redirect(url_for('forum'))

# Добавление комментария к посту на форуме
@app.route('/add_comment/<int:post_id>', methods=['POST'])
@login_required
def add_comment(post_id):
    post = ForumPost.query.get_or_404(post_id)
    form = ForumCommentForm()
    if form.validate_on_submit():
        new_comment = ForumComment(
            content=form.content.data,
            user=current_user,
            post=post,
            post_id=form.post_id.data
        )
        db.session.add(new_comment)
        db.session.commit()
        flash('Комментарий добавлен успешно!', 'success')
    else:
        flash('Ошибка при добавлении комментария', 'danger')

    return redirect(url_for('forum_post', post_id=post.id))

# Получение JWT-токена
@app.route('/get_token')
def get_token():
    if current_user.is_authenticated:
        access_token = create_access_token(identity=current_user.id)
        return jsonify(access_token=access_token), 200
    else:
        return jsonify(message="Неверные учетные данные"), 401