import telegram
from utils import (get_smile, play_random_numbers,
                   main_keyboard, has_object_on_image)

from jobs import alarm

from models import add_user_db, subscribe_user, add_vote, rating
from telegram import Update
from telegram.ext import ContextTypes
import os


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user_name = update.effective_user.first_name
    add_user_db(user_name, chat_id)

    context.user_data['emoji'] = get_smile(context.user_data)
    await update.message.reply_text(
        f'Привет {user_name} {context.user_data["emoji"]}',
        reply_markup=main_keyboard()
        )


async def guess(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.args:
        try:
            user_number = int(context.args[0])
            message = play_random_numbers(user_number)
        except ValueError as vlerror:
            print(repr(vlerror), 'must be int')
    else:
        message = 'Введите целое число'
    await update.message.reply_text(
        text=message,
        reply_markup=main_keyboard()
    )


async def user_coordinatenes(
                update: Update,
                context: ContextTypes.DEFAULT_TYPE
                            ):

    smile = get_smile(context.user_data)

    location = update.message.location

    latitude = location.latitude
    longitude = location.longitude
    await update.message.reply_text(
        text=f"""Latitude: {latitude}, Longitude: {longitude} {smile}""",
        reply_markup=main_keyboard()
    )


async def check_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_photo = update.message.photo[-1]
    await update.message.reply_text('Обработка фото')
    os.makedirs('downloads', exist_ok=True)

    photo_File = await context.bot.getFile(user_photo.file_id)

    file_split = photo_File.file_path.split('/')[-1]
    format_file = file_split.split('.')[-1]

    file_name = os.path.join(
        'downloads', f'{user_photo.file_id}.{format_file}'
                            )

    await telegram.File.download(photo_File, file_name)
    await update.message.reply_text('Фото сохранено')
    if has_object_on_image(file_name):
        await update.message.reply_text('Найден кисик')
        new_file_name = os.path.join(
            'downloads', f'{user_photo.file_id}.{format_file}'
                                    )
        os.rename(file_name, new_file_name)
    else:
        os.remove(file_name)
        await update.message.reply_text('Кисик не найден')


async def sub(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user_name = update.effective_user.first_name
    try:
        add_user_db(user_name=user_name, chat_id=chat_id)
    finally:
        subscribe_user(chat_id, True)

    await update.message.reply_text(
        text='Вы подписались'
    )


async def unsub(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    subscribe_user(chat_id, False)

    await update.message.reply_text(
        text='Вы отписались'
    )


async def set_alarm(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.message.chat_id
    try:
        alarm_seconds = abs(int(context.args[0]))
        await update.message.reply_text(
            text=f'Уведомление через {alarm_seconds} секунд')
        context.job_queue.run_once(
            alarm, alarm_seconds, chat_id=chat
        )
    except (Exception) as ex:
        await update.message.reply_text(
            text='Введите целое число секунд после команды'
        )
        print(repr(ex))


async def picture_ranting(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()

    user_id = update.effective_chat.id
    user_choise = update.callback_query.data
    image, vote = user_choise.split('|')[1:]
    vote = int(vote)

    add_vote(user_id, image, vote)
    rating_picture = rating(image)

    await update.callback_query.edit_message_caption(
        caption=f'Thank you, rating - {rating_picture}'
    )
