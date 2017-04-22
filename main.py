import telebot  # Основная библиотека для работы с Bot API

from datetime import datetime

import bot_token  # Файл с объявлением токена спрятан с помощью .gitignore
import quotes  # Все фразы бота
import parsing  # Функции для работы с текстом и хранилищем
import database  # Функции для работы с базой данных
import exceptions  # Различные виды исключений


bot = telebot.TeleBot(bot_token.token)
print(bot.get_me())


@bot.message_handler(commands=['start', 'help'])
def handle_text(message):
    bot.send_message(message.chat.id, quotes.help_text, parse_mode='Markdown')


@bot.message_handler(commands=['add'])
def handle_text(message):
    try:
        arguments = parsing.find_arguments(message.text, last_is_string=True)
        cost = str(int(arguments[0]))
        date = str(datetime.strptime(arguments[1], '%d.%m.%y'))
        description = arguments[2]
        database.add(message.chat.id, cost, date, description)
        bot.send_message(message.chat.id, quotes.add_ok)
    except exceptions.WrongNumberOfArgumentsException as exception:
        bot.send_message(message.chat.id, exception.value)
    except BaseException:
        bot.send_message(message.chat.id, quotes.unexpected_error)


# remove


# change


@bot.message_handler(commands=['show'])
def handle_text(message):
    try:
        bot.send_message(message.chat.id,
                         database.find_records(message.chat.id))
    except BaseException:
        bot.send_message(message.chat.id, quotes.unexpected_error)


bot.polling(none_stop=True, interval=0)
