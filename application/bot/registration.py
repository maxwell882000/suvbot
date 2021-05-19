from application import telegram_bot
from application.core import userservice
from application.resources import strings, keyboards
from application.utils import bot as botutils
from telebot.types import Message
import re


def request_registration_phone_number_handler(message: Message, **kwargs):
    chat_id = message.chat.id
    user_id = message.from_user.id
    name = kwargs.get('name')
    language = 'ru'

    def error():
        if message.text == '/start':
            welcome(message)
            return
        error_msg = strings.get_string('registration.request.phone_number', language)
        telegram_bot.send_message(chat_id, error_msg, parse_mode='HTML')
        telegram_bot.register_next_step_handler_by_chat_id(chat_id, request_registration_phone_number_handler, name=name, language=language)

    if message.contact is not None:
        phone_number = message.contact.phone_number
    else:
        if message.text is None:
            error()
            return
        else:
            match = re.match(r'\+*998\s*\d{2}\s*\d{3}\s*\d{2}\s*\d{2}', message.text)
            if match is None:
                error()
                return
            phone_number = match.group()
    userservice.register_user(user_id, message.from_user.username, name, phone_number, language)
    success_message = strings.get_string("welcome.registration_successfully", language)
    botutils.to_main_menu(chat_id, language, success_message)


def process_user_language(message: Message):
    language = 'ru'
    request_registration_handler(message, language)


@telegram_bot.message_handler(commands=['start'], func=lambda m: m.chat.type == 'private')
def welcome(message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    current_user = userservice.get_user_by_telegram_id(user_id)
    if current_user:
        botutils.to_main_menu(chat_id, current_user.language)
        return
    process_user_language(message)


def request_registration_handler(message: Message, language: str):
    chat_id = message.chat.id

    welcome_message = strings.get_string('registration.request.welcome', language)
    remove_keyboard = keyboards.get_keyboard('remove')
    telegram_bot.send_message(chat_id, welcome_message, reply_markup=remove_keyboard)
    telegram_bot.register_next_step_handler_by_chat_id(chat_id, request_registration_name_handler, language=language)


def request_registration_name_handler(message: Message, **kwargs):
    chat_id = message.chat.id
    language = kwargs.get('language')

    def error():
        if message.text == '/start':
            welcome(message)
            return
        error_msg = strings.get_string('registration.request.welcome', language)
        telegram_bot.send_message(chat_id, error_msg)
        telegram_bot.register_next_step_handler_by_chat_id(chat_id, request_registration_name_handler,
                                                           language=language)

    if not message.text:
        error()
        return
    name = message.text
    phone_number_message = strings.get_string('registration.request.phone_number', language)
    phone_number_keyboard = keyboards.from_user_phone_number(language, go_back=False)
    telegram_bot.send_message(chat_id, phone_number_message, parse_mode='HTML', reply_markup=phone_number_keyboard)
    telegram_bot.register_next_step_handler_by_chat_id(chat_id, request_registration_phone_number_handler, name=name,
                                                       language=language)
