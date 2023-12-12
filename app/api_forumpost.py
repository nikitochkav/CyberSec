"""
Модульное описание:
    Этот модуль определяет веб-приложение Flask с конечными точками RESTful API для управления сообщениями на форуме.
"""

from flask import Flask, jsonify
from flask_restful import Api, Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import app, db
from app.models import ForumPost

api = Api(app)

class ForumPostsResource(Resource):
    """
    Класс ForumPostsResource обрабатывает запросы, связанные с несколькими сообщениями на форуме.
    """

    @jwt_required()
    def get(self):
        """
        Обрабатывает GET-запрос для получения всех сообщений на форуме.

        Возвращает:
            JSON: Список сообщений на форуме.
        """
        current_user_id = get_jwt_identity()
        posts = ForumPost.query.all()
        post_list = [
            {
                'id': post.id,
                'title': post.title,
                'content': post.content,
                'user_id': post.user_id,
                'timestamp': post.timestamp
            } for post in posts
        ]
        return jsonify({'forum_posts': post_list})

class ForumPostResource(Resource):
    """
    Класс ForumPostResource обрабатывает запросы, связанные с одним сообщением на форуме.
    """

    @jwt_required()
    def get(self, post_id):
        """
        Обрабатывает GET-запрос для получения конкретного сообщения на форуме.

        Аргументы:
            post_id (int): Идентификатор сообщения на форуме для получения.

        Возвращает:
            JSON: Подробности запрошенного сообщения на форуме.
        """
        current_user_id = get_jwt_identity()
        post = ForumPost.query.get_or_404(post_id)
        post_data = {
            'id': post.id,
            'title': post.title,
            'content': post.content,
            'user_id': post.user_id,
            'timestamp': post.timestamp
        }
        return jsonify({'forum_post': post_data})

api.add_resource(ForumPostsResource, '/api/forum_posts')
api.add_resource(ForumPostResource, '/api/forum_posts/<int:post_id>')
