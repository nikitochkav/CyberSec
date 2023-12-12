from flask import Flask, current_app
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from app import app, db, login_manager
from datetime import datetime


def load_user(user_id):
    """
    Загрузка пользователя по ID.
    """
    return User.query.get(int(user_id))


class User(db.Model):
    """
    Модель пользователя.
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(20), default='user')

    def __repr__(self):
        return f'<User {self.email}>'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_active(self):
        return True

    def get_id(self):
        return str(self.id)

    def is_admin(self):
        return self.role == 'admin'

    def is_authenticated(self):
        return True


class Service(db.Model):
    """
    Модель сервиса.
    """
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(255), nullable=True)


class Attack(db.Model):
    """
    Модель атаки.
    """
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(255), nullable=False)
    count = db.Column(db.Integer, nullable=False)


class ForumPost(db.Model):
    """
    Модель поста на форуме.
    """
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('forumposts', lazy=True))

    def __repr__(self):
        return f"ForumPost('{self.title}', '{self.timestamp.strftime('%Y-%m-%d %H:%M:%S.%f')}')"


class ForumComment(db.Model):
    """
    Модель комментария на форуме.
    """
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('forum_post.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('forum_comments', lazy=True))
    post = db.relationship('ForumPost', backref=db.backref('comments', lazy=True))


with app.app_context():
    inspector = db.inspect(db.engine)
    existing_tables = inspector.get_table_names()

    if 'user' not in existing_tables:
        db.create_all()

        if not Service.query.count():
            service1 = Service(title='Антивирусная Защита',
                               description='Мощные антивирусные решения для защиты от вредоносных программ.',
                               image='service1.jpg')
            service2 = Service(title='Защита от DDoS-атак',
                               description='Мы предоставляем услуги по обнаружению и предотвращению DDoS-атак.',
                               image='service2.jpg')
            service3 = Service(title='Киберспецназ',
                               description='Наш киберспецназ готов реагировать на любые инциденты безопасности.',
                               image='service3.jpg')

            db.session.add_all([service1, service2, service3])

        if not Attack.query.count():
            attack1 = Attack(type='Фишинг', count=15)
            attack2 = Attack(type='DDoS', count=10)
            attack3 = Attack(type='APT', count=8)
            attack4 = Attack(type='Социальная инженерия', count=12)
            attack5 = Attack(type='Мальвара', count=7)

            db.session.add_all([attack1, attack2, attack3, attack4, attack5])

        db.session.commit()
