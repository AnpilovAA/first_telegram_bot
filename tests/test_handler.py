from conftest import make_message, call_handler
from handlers import talk_to_me


def test_talk_to_me(updater, effective_user_telegram_user):
    message = make_message('Hi', effective_user_telegram_user, updater)
    call_handler(updater, talk_to_me, message)
    message.reply_text
    assert message.reply_text
