from datetime import time

import logging
from pytz import timezone
from telegram.ext import (ApplicationBuilder, CommandHandler, filters,
                          MessageHandler, ConversationHandler,
                          CallbackQueryHandler)

from handlers import (set_alarm, start, check_photo, user_coordinatenes, guess,
                      sub, unsub, picture_ranting)
from jobs import send_updates
from utils import send_picture
from anketa import (anketa_start, anketa_name, anketa_rating,
                    anketa_comment, anketa_skip, anketa_dontknow)
from settings import TOKEN


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)


if __name__ == "__main__":
    application = ApplicationBuilder().token(TOKEN).build()

    job_queue = application.job_queue

    target_time = time(12, 0, tzinfo=timezone('Europe/Moscow'))
    job_daily = job_queue.run_daily(send_updates,
                                    target_time,
                                    days=(1, 2, 3, 5))

    job_send = job_queue.run_repeating(send_updates,
                                       interval=10,
                                       first=1,
                                       last=1)

    anketa = ConversationHandler(
        entry_points=[
            MessageHandler(filters.Regex('^(Заполнить анкету)$'), anketa_start)
        ],

        states={
            'name': [MessageHandler(filters.TEXT, anketa_name)],

            'rating': [MessageHandler(
                filters.Regex('^(1|2|3|4|5)$'), anketa_rating
                                     )],

            'comment': [
                CommandHandler('skip', anketa_skip),
                MessageHandler(filters.TEXT, anketa_comment)
            ]
        },

        fallbacks=[
            MessageHandler(filters.ALL, anketa_dontknow)
        ]
    )

    start_handler = CommandHandler('start', start)

    send_picture_handler = CommandHandler('picture', send_picture)

    alarm_handler = CommandHandler('alarm', set_alarm)

    subscribe_handler = CommandHandler('subscribe', sub)
    unsubscribe_handler = CommandHandler('unsubscribe', unsub)

    regex_handler = MessageHandler(
        filters.Regex('^(Прислать слёзы)$'), send_picture
        )

    check_user_photo = MessageHandler(filters.PHOTO, check_photo)

    location_handler = MessageHandler(filters.LOCATION, user_coordinatenes)

    guess_handler = CommandHandler('guess', guess)

    callback_query_handler = CallbackQueryHandler(
        picture_ranting,
        pattern='^(rating|)'
        )

    application.add_handlers((
        start_handler,
        guess_handler,
        send_picture_handler,
        regex_handler,
        location_handler,
        check_user_photo,
        anketa,
        subscribe_handler,
        unsubscribe_handler,
        alarm_handler,
        callback_query_handler,
        ))

    application.run_polling()
