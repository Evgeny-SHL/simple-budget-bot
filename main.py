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
        date = str(datetime.strptime(arguments[1], '%y-%m-%d'))[2:10]
        description = arguments[2]
        database.add(message.chat.id, cost, date, description)
        bot.send_message(message.chat.id, quotes.add_ok)
    except exceptions.WrongNumberOfArgumentsException as exception:
        bot.send_message(message.chat.id, exception.value)
    except BaseException:
        bot.send_message(message.chat.id, quotes.unexpected_error)


@bot.message_handler(commands=['remove'])
def handle_text(message):
    try:
        arguments = parsing.find_arguments(message.text)
        record_id = str(int(arguments[0]))
        database.remove(message.chat.id, record_id)
        bot.send_message(message.chat.id, quotes.remove_ok)
    except exceptions.WrongNumberOfArgumentsException as exception:
        bot.send_message(message.chat.id, exception.value)
    except exceptions.NoSuchRecordExcpetion as exception:
        bot.send_message(message.chat.id, exception.value)
    except BaseException:
        bot.send_message(message.chat.id, quotes.unexpected_error)


@bot.message_handler(commands=['change'])
def handle_text(message):
    try:
        arguments = parsing.find_arguments(message.text)
        record_id = str(int(arguments[0]))
        cost = str(int(arguments[1]))
        try:
            date = str(datetime.strptime(arguments[2], '%y-%m-%d'))[2:10]
        except BaseException:
            raise exceptions.InvalidDateException
        description = arguments[3]
        database.change(message.chat.id, record_id, cost, date, description)
        bot.send_message(message.chat.id, quotes.change_ok)
    except exceptions.WrongNumberOfArgumentsException as exception:
        bot.send_message(message.chat.id, exception.value)
    except exceptions.NoSuchRecordExcpetion as exception:
        bot.send_message(message.chat.id, exception.value)
    except exceptions.InvalidDateException as exception:
        bot.send_message(message.chat.id, exception.value)
    except BaseException:
        bot.send_message(message.chat.id, quotes.unexpected_error)


@bot.message_handler(commands=['show'])
def handle_text(message):
    try:
        bot.send_message(message.chat.id,
                         database.find_records(message.chat.id))
    except BaseException:
        bot.send_message(message.chat.id, quotes.unexpected_error)


@bot.message_handler(commands=['total'])
def handle_text(message):
    try:
        bot.send_message(message.chat.id,
                         database.find_total_outcome(message.chat.id))
    except BaseException:
        bot.send_message(message.chat.id, quotes.unexpected_error)


@bot.message_handler(commands=['last'])
def handle_text(message):
    try:
        arguments = parsing.find_arguments(message.text)
        number = int(arguments[0])
        if number <= 0:
            raise BaseException
        unit = str(arguments[1])
        if unit not in ['дн', 'нед', 'мес']:
            raise exceptions.InvalidUnitException
        bot.send_message(message.chat.id,
                         database.recently_outcome(message.chat.id, number,
                                                   unit))
    except exceptions.WrongNumberOfArgumentsException as exception:
        bot.send_message(message.chat.id, exception.value)
    except exceptions.InvalidUnitException as exception:
        bot.send_message(message.chat.id, exception.value)
    except BaseException:
        bot.send_message(message.chat.id, quotes.unexpected_error)


@bot.message_handler(commands=['clear'])
def handle_text(message):
    try:
        arguments = parsing.find_arguments(message.text)
        try:
            date = str(datetime.strptime(arguments[0], '%y-%m-%d'))[2:10]
        except BaseException:
            raise exceptions.InvalidDateException
        database.clear_before_date(message.chat.id, date)
        bot.send_message(message.chat.id, quotes.clear_ok)
    except exceptions.WrongNumberOfArgumentsException as exception:
        bot.send_message(message.chat.id, exception.value)
    except exceptions.InvalidDateException as exception:
        bot.send_message(message.chat.id, exception.value)
    except BaseException:
        bot.send_message(message.chat.id, quotes.unexpected_error)


bot.polling(none_stop=True, interval=0)
