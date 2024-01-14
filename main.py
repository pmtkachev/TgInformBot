import requests as req
import telebot

API_TOKEN = 'your_token'

bot = telebot.TeleBot(API_TOKEN)


def get_currency_base():
    resp = req.get('http://www.cbr.ru/scripts/XML_daily.asp')
    print(resp.text)


@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, 'Hi, I am bot')


@bot.message_handler(func=lambda message: True)
def echo_message(message):
    bot.reply_to(message, message.text)


# bot.infinity_polling()
get_currency_base()
