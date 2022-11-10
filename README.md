# Telegram bot

Hello this is studiet project.\
Here I am learned using as main libraries:\
**python-telegram-bot**\
**sqlalchemy**
____
Before start project you have to create settings.py\
with settings:\
- TOKEN = "yours telegram token"
- USER_EMOJI = [yours emoji(s)] 
- CLARIFAI_API_KEY = "yours key"
- DATABASE = "yours data base"
- PATH_TO_PHOTO = "path_to_ you_dir_with_photo\\*(photo_name).format"
________
## Features

In this bot I made 3 buttons that appear after the /start command

- Send a picture
- My location
- Fill in the form

## -Send picture
    If you press Send picture bot will send you picture with inline button.
    Where you could vote for picture "Like" or "Dislike".
    After that bot send you rating of the picture

## - My location
    You just send your location to bot and he send you longitude and latitude

## - Fill form
    Its conversation with bot, bot send you question and take user answer.
    And after fill form he send you back  your information