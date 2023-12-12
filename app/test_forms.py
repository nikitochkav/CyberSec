from flask_testing import TestCase
from flask import Flask
from app import app
from app.forms import RegistrationForm, LoginForm


class TestForms(TestCase):
    """
    Класс тестирования форм в приложении Flask.
    """

    def create_app(self):
        """
        Создание Flask-приложения для тестирования.
        """
        app.config['WTF_CSRF_ENABLED'] = False
        return app

    def test_registration_form(self):
        """
        Тест формы регистрации.
        """
        form = RegistrationForm(
            username="testuser",
            email="test@example.com",
            password="testpassword",
            confirm_password="testpassword",
            admin=True
        )
        self.assertTrue(form.validate(), f"Ошибка валидации формы: {form.errors}")

    def test_login_form(self):
        """
        Тест формы входа.
        """
        form = LoginForm(
            email="test@example.com",
            password="testpassword"
        )
        self.assertTrue(form.validate(), f"Ошибка валидации формы: {form.errors}")


if __name__ == '__main__':
    import unittest
    unittest.main()
