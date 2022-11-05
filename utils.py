from glob import glob
from random import randint, choice
from emoji import emojize
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes

from settings import USER_EMOJI, CLARIFAI_API_KEY

from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api import resources_pb2, service_pb2, service_pb2_grpc
from clarifai_grpc.grpc.api.status import status_pb2, status_code_pb2


def get_smile(user_data):
    if 'emoji' not in user_data:
        smile = choice(USER_EMOJI)
        return emojize(smile, language='alias')
    return user_data['emoji']


def play_random_numbers(user_number):
    bot_number = randint(user_number - 10, user_number + 10)
    if user_number > bot_number:
        message = f'Вы победили ваше число {user_number},\
             число бота {bot_number}'
    elif user_number == bot_number:
        message = f'Ничья ваше число {user_number}, число бота {bot_number}'
    else:
        message = message = f'Вы проиграли число {user_number},\
             число бота {bot_number}'
    return message


async def send_picture(update: Update, context: ContextTypes.DEFAULT_TYPE):
    any_photo_list = glob(r'C:\Users\Public\Pictures\*.jp*g')
    any_photo_filename = choice(any_photo_list)
    chat_id = update.effective_chat.id
    await context.bot.send_photo(
        chat_id=chat_id,
        photo=open(any_photo_filename, 'rb')
    )


def main_keyboard():
    # return ReplyKeyboardMarkup([['Прислать слёзы', 'Test']]) # Create main keyboard
    return ReplyKeyboardMarkup([
        ['Прислать слёзы', KeyboardButton('Моя локация', request_location=True), "Заполнить анкету"]
        ])  # Create main keyboard


def has_object_on_image(file_name, object_name):
    chanel = ClarifaiChannel.get_grpc_channel()
    app = service_pb2_grpc.V2Stub(chanel)
    metadata = (('authorization', f'Key {CLARIFAI_API_KEY}'),)

    with open(file_name, 'rb') as f:
        file_data = f.read()
        image = resources_pb2.Image(base64=file_data)

    request = service_pb2.PostModelOutputsRequest(
        model_id='aaa03c23b3724a16a56b629203edc62c',
        inputs=[
            resources_pb2.Input(data=resources_pb2.Data(image=image))
        ]
    )
    response = app.PostModelOutputs(request, metadata=metadata)
    return check_response_for_object(response, object_name)


def check_response_for_object(response, object_name):
    if response.status.code == status_code_pb2.SUCCESS:
        for concept in response.outputs[0].data.concepts:
            if concept.name == object_name and concept.value >= 0.9:
                return True
    else:
        print(f'Ошибка {response.outputs[0].status.details}')
    return False


if __name__ == '__main__':
    print(has_object_on_image(r'downloads\1.jpg', 'cat'))
    print(has_object_on_image(r'downloads\2.jpg', 'people'))
    print(has_object_on_image(r'downloads\3.jpg', 'cat'))
