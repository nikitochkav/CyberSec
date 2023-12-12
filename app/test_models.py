import os
import sys
from datetime import datetime

import pytest
from app.models import User, ForumPost


@pytest.fixture
def sample_user():
    """
    Фикстура для создания образца пользователя для тестирования.
    """
    user = User(username='testuser', email='testuser@example.com')
    user.set_password('testpassword')
    return user


@pytest.fixture
def sample_forum_post(sample_user):
    """
    Фикстура для создания образца ForumPost для тестирования.
    """
    return ForumPost(
        title='Test ForumPost',
        content='Test Description',
        timestamp=datetime.utcnow(),
        user_id=sample_user
    )


def test_user_creation(sample_user):
    """
    Тест создания объекта User.
    """
    assert sample_user.username == 'testuser'
    assert sample_user.email == 'testuser@example.com'
    assert sample_user.check_password('testpassword')


def test_forum_post_creation(sample_forum_post, sample_user):
    """
    Тест создания объекта ForumPost.
    """
    assert sample_forum_post.title == 'Test ForumPost'
    assert sample_forum_post.content == 'Test Description'
    assert sample_forum_post.timestamp
    assert sample_forum_post.user_id == sample_user


def test_forum_post_representation(sample_forum_post):
    """
    Тест строкового представления объекта ForumPost.
    """
    assert repr(sample_forum_post) == f"ForumPost('Test ForumPost', '{sample_forum_post.timestamp}')"


def test_user_representation(sample_user):
    """
    Тест строкового представления объекта User.
    """
    assert repr(sample_user) == f"<User testuser@example.com>"
