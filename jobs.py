from datetime import datetime
from telegram.ext import ContextTypes
from telegram.error import BadRequest
from models import get_subscribe


async def send_updates(context: ContextTypes.DEFAULT_TYPE):
    now = datetime.now().strftime('%d.%m.%Y %H:%M:%S')

    for user in get_subscribe():
        try:
            await context.bot.send_message(
                chat_id=user.user_id,
                text=f'Точное время {now}'
                )
        except BadRequest:
            print(f'User {user.user_id} not found in database')


async def alarm(context: ContextTypes.DEFAULT_TYPE):
    print('Alarm----', context.job.chat_id)
    try:
        await context.bot.send_message(
            chat_id=context.job.chat_id,
            text='Сработал будильник'
        )
    except Exception as ex:
        print('alarm --------', ex)