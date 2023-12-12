import os
import sys

import pytest
from flask import Flask
from app import app, db


@pytest.fixture
def client():
    """
    Фикстура для Flask тестового клиента.

    Настраивает тестовое окружение с базой данных SQLite в памяти.

    Возвращает:
        Flask тестовый клиент: Тестовый клиент для выполнения запросов.

    После выполнения теста очищает тестовое окружение.
    """
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    client = app.test_client()

    with app.app_context():
        db.create_all()

    yield client

    with app.app_context():
        db.drop_all()


def make_request(client, endpoint):
    """
    Выполняет запрос к указанной конечной точке с использованием заданного клиента.

    Аргументы:
        client (Flask тестовый клиент): Тестовый клиент для выполнения запросов.
        endpoint (str): Конечная точка для выполнения запроса.

    Возвращает:
        str: Декодированные данные ответа.
    """
    return client.get(endpoint).data.decode('utf-8')


def test_index(client):
    """
    Тест маршрута индекса.

    Аргументы:
        client (Flask тестовый клиент): Тестовый клиент для выполнения запросов.
    """
    response = make_request(client, '/')
    print(response)
    assert 'Главная' in response


def test_about(client):
    """
    Тест маршрута о компании.

    Аргументы:
        client (Flask тестовый клиент): Тестовый клиент для выполнения запросов.
    """
    response = make_request(client, '/about')
    assert 'О компании' in response


def test_contact(client):
    """
    Тест маршрута контактов.

    Аргументы:
        client (Flask тестовый клиент): Тестовый клиент для выполнения запросов.
    """
    response = make_request(client, '/contact')
    assert 'Контакты' in response
