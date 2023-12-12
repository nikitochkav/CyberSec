import os
from decouple import config


class Config:
    """
    Класс конфигурации для приложения.

    Атрибуты:
        SECRET_KEY (str): Секретный ключ для Flask-приложения.
        SQLALCHEMY_DATABASE_URI (str): URI базы данных для SQLAlchemy.
        SQLALCHEMY_TRACK_MODIFICATIONS (bool): Конфигурация отслеживания изменений в SQLAlchemy.
        DEBUG (bool): Конфигурация режима отладки.

        MAIL_USERNAME (str): Имя пользователя электронной почты для отправки писем.
        MAIL_PASSWORD (str): Пароль электронной почты для отправки писем.
        MAIL_SERVER (str): SMTP-сервер для отправки писем.
        MAIL_PORT (int): Порт SMTP-сервера.
        MAIL_USE_SSL (bool): Использовать SSL для SMTP-сервера.
        MAIL_USE_TLS (bool): Использовать TLS для SMTP-сервера.
    """

    SECRET_KEY = config('SECRET_KEY', default='your_default_secret_key')
    SQLALCHEMY_DATABASE_URI = config('DATABASE_URL', default='sqlite:///your_database.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True

    MAIL_USERNAME = config('MAIL_USERNAME', default='your_email@example.com')
    MAIL_PASSWORD = config('MAIL_PASSWORD', default='your_email_password')
    MAIL_SERVER = 'smtp.yandex.ru'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USE_TLS = False
