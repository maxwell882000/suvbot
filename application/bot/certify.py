from application import telegram_bot
from application.core import userservice
from application.resources import strings
from application.utils import bot as botutlis
from telebot.types import Message
from . import Config
import settings


def check_about(message: Message):
    if not message.text:
        return False
    user_id = message.from_user.id
    user = userservice.get_user_by_telegram_id(user_id)
    if not user:
        return False
    language = user.language
    return strings.get_string('main_menu.about', language) in message.text and message.chat.type == 'private'


def checker(message: Message):
    if not message.text:
        return False
    return botutlis.check_auth(message) and check_about(message)


@telegram_bot.message_handler(commands=['about'])
@telegram_bot.message_handler(content_types=['text'], func=checker)
def about_handler(message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    language = userservice.get_user_language(user_id)
    # about_text = settings.get_about_text('ru')
    # telegram_bot.send_message(chat_id, about_text)
    for num in range(3):
        photo = open((Config.CERTIFY_DIRECTORY + str(num) + '.jpg'), 'rb')
        telegram_bot.send_photo(chat_id, photo=photo)
    botutlis.to_main_menu(chat_id, language)
