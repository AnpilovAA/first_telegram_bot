from telegram import Update, ReplyKeyboardRemove, ReplyKeyboardMarkup
from telegram.constants import ParseMode
from telegram.ext import ContextTypes, ConversationHandler

from models import add_anketa

from utils import main_keyboard


async def anketa_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    await message.reply_text(
        'Hello, what is your name and lastname?',
        reply_markup=ReplyKeyboardRemove()
    )
    return 'name'


async def anketa_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    user_name = update.message.text
    if len(user_name.split()) < 2:
        await message.reply_text(
            text='Please input your name and last name'
        )
        return 'name'
    else:
        context.user_data['anketa'] = {'name': user_name}
        reply_keyboard = [['1', '2', '3', '4', '5']]
        await message.reply_text(
            'Please rate our bot from 1 to 5',
            reply_markup=ReplyKeyboardMarkup(
                reply_keyboard,
                one_time_keyboard=True
                )
        )
        return 'rating'


async def anketa_rating(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['anketa']['rating'] = int(update.message.text)
    await update.message.reply_text(
        'Write a comment or press /skip'
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
    user_text = f""" <b>Name </b> {anketa['name']}
    <b> Score </b> {anketa['rating']}
    """
    if 'comment' in anketa:
        user_text += f"<b>Comment</b> {anketa['comment']}"
    return user_text


async def anketa_dontknow(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Sorry I don't understand")
