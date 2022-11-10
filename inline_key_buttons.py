from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def inline_key_button(filename):
    callback_text = f'rating|{filename}|'
    name = ['Like', 'Dislike']
    value = ['1', '-1']

    key_button = [
        [
            InlineKeyboardButton(name[0],
                                 callback_data=callback_text + value[0]),
            InlineKeyboardButton(name[1],
                                 callback_data=callback_text + value[1])
        ]
    ]
    return InlineKeyboardMarkup(key_button)
