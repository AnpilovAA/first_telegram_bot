from telegram import Update, ReplyKeyboardRemove, ReplyKeyboardMarkup
from telegram.constants import ParseMode
from telegram.ext import ContextTypes, ConversationHandler

from models import add_anketa

from utils import main_keyboard


async def anketa_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    await message.reply_text(
        'Привет, как вас зовут?',
        reply_markup=ReplyKeyboardRemove()
    )
    return 'name'


async def anketa_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    user_name = update.message.text
    if len(user_name.split()) < 2:
        await message.reply_text(
            text='Пожалуйста введите имя и фамилию'
        )
        return 'name'
    else:
        context.user_data['anketa'] = {'name': user_name}
        reply_keyboard = [['1', '2', '3', '4', '5']]
        await message.reply_text(
            'Пожалуйста оцените нашего бота от 1 до 5',
            reply_markup=ReplyKeyboardMarkup(
                reply_keyboard,
                one_time_keyboard=True
                )
        )
        return 'rating'


async def anketa_rating(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['anketa']['rating'] = int(update.message.text)
    await update.message.reply_text(
        'Напишите комментарий или нажмите /skip'
    )
    return 'comment'


async def anketa_comment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['anketa']['comment'] = update.message.text
    user_text = await format_anketa(context.user_data['anketa'])
    id = update.effective_chat.id

    anketa = context.user_data['anketa']
    add_anketa(
            user_name=anketa['name'],
            user_id=id,
            rating=anketa['rating'],
            user_comment=anketa['comment'])

    await update.message.reply_text(
        user_text,
        parse_mode=ParseMode.HTML,
        reply_markup=main_keyboard()
    )
    return ConversationHandler.END


async def anketa_skip(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['anketa']['comment'] = update.message.text
    anketa = context.user_data['anketa']
    id = update.effective_chat.id

    add_anketa(
        user_name=anketa['name'],
        user_id=id,
        rating=anketa['rating'],
        user_comment=''
    )
    user_text = await format_anketa(context.user_data['anketa'])
    await update.message.reply_text(
        user_text,
        parse_mode=ParseMode.HTML,
        reply_markup=main_keyboard()
    )
    return ConversationHandler.END


async def format_anketa(anketa):
    user_text = f""" <b> Имя Фамилия </b> {anketa['name']}
    <b> Оценка </b> {anketa['rating']}
    """
    if 'comment' in anketa:
        user_text += f"<b>Комментарий</b> {anketa['comment']}"
    return user_text


async def anketa_dontknow(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Я вас не понимаю')
