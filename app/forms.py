from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo, Length


class ContactForm(FlaskForm):
    """
    Форма для обратной связи.

    Attributes:
        name (StringField): Поле для ввода имени (обязательное).
        email (StringField): Поле для ввода адреса электронной почты (обязательное, с валидацией).
        message (StringField): Поле для ввода сообщения (обязательное).
        submit (SubmitField): Кнопка отправки формы.
    """
    name = StringField('Имя', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    message = StringField('Сообщение', validators=[DataRequired()])
    submit = SubmitField('Отправить')


class LoginForm(FlaskForm):
    """
    Форма для входа в систему.

    Attributes:
        email (StringField): Поле для ввода адреса электронной почты (обязательное, с валидацией).
        password (PasswordField): Поле для ввода пароля (обязательное).
        submit (SubmitField): Кнопка входа.
    """
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')


class RegistrationForm(FlaskForm):
    """
    Форма для регистрации нового пользователя.

    Attributes:
        username (StringField): Поле для ввода имени пользователя (обязательное).
        email (StringField): Поле для ввода адреса электронной почты (обязательное, с валидацией).
        password (PasswordField): Поле для ввода пароля (обязательное).
        confirm_password (PasswordField): Поле для подтверждения пароля (обязательное, сравнивается с основным паролем).
        admin (BooleanField): Поле для указания, является ли пользователь администратором.
        submit (SubmitField): Кнопка регистрации.
    """
    username = StringField('Имя пользователя', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    confirm_password = PasswordField('Подтвердить пароль', validators=[DataRequired(), EqualTo('password')])
    admin = BooleanField('Администратор')
    submit = SubmitField('Зарегистрироваться')


class ForumPostForm(FlaskForm):
    """
    Форма для создания нового поста на форуме.

    Attributes:
        title (StringField): Поле для ввода заголовка поста (обязательное).
        content (TextAreaField): Поле для ввода содержания поста (обязательное).
        search_input (StringField): Поле для ввода текста поиска (необязательное, ограничено в длине).
        submit (SubmitField): Кнопка отправки формы.
    """
    title = StringField('Заголовок', validators=[DataRequired()])
    content = TextAreaField('Содержание', validators=[DataRequired()])
    search_input = StringField('Поиск', validators=[Length(max=255)])
    submit = SubmitField('Post')


class ForumCommentForm(FlaskForm):
    """
    Форма для создания нового комментария к посту на форуме.

    Attributes:
        content (TextAreaField): Поле для ввода текста комментария (обязательное).
        post_id (IntegerField): Поле для ввода ID поста, к которому добавляется комментарий (обязательное).
        submit (SubmitField): Кнопка отправки формы.
    """
    content = TextAreaField('Комментарий', validators=[DataRequired()])
    post_id = IntegerField('ID поста', validators=[DataRequired()])
    submit = SubmitField('Comment')
