import telebot  # Основаня библиотека для работы с Bot API

import bot_token  # Файл с объявление токена спрятан с помощью .gitignore
import quotes  # Все фразы бота

# from datetime import datetime

bot = telebot.TeleBot(bot_token.token)

print(bot.get_me())

@bot.message_handler(commands=['start'])
def handle_text(message):
    pass

@bot.message_handler(commands=['help'])
def handle_text(message):
    bot.send_message(message.chat.id, quotes.help_text)

bot.polling(none_stop=True, interval=0)
