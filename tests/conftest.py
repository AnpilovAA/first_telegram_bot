from pytest_sqlalchemy_mock.base import pytest
from mock_data import MockData
from unittest.mock import Mock
from models import Base

from datetime import datetime


from telegram import Bot, User, Update, Message, Chat
from telegram.ext import CallbackContext


@pytest.fixture(scope="function")
def sqlalchemy_declarative_base():
    return Base


@pytest.fixture(scope='function')
def sqlalchemy_mock_config():
    return [('users', MockData.USER_DATA)]


@pytest.fixture
def effective_user():
    class EffectiveUser:
        def __init__(self, user_name, user_id):
            self.user_name = user_name
            self.user_id = user_id
    return EffectiveUser('Fake', 33215632)


@pytest.fixture
def effective_user_telegram_user():
    return User(id=123, first_name='Faker', is_bot=False)


@pytest.fixture
def updater():
    token = 11221
    return Update(update_id=token)


@pytest.fixture
def tele_bot():
    return Bot(token='12211')


def make_message(text, user, bot):
    chat = Chat(id=1, type='PRIVATE')
    message = Message(
        message_id=1,
        from_user=user,
        date=datetime.now(),
        chat=chat,
        text=text,
        bot=tele_bot
    )
    message.reply_text is Mock(return_value=None)
    return message


def call_handler(aplication, handler, message):
    update = Update(update_id=1, message=message)
    context = CallbackContext.from_update(update, application=aplication)
    return handler(update, context)
