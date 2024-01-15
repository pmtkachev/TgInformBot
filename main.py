from datetime import datetime

import requests as req
import telebot

API_TOKEN = 'your_token'

bot = telebot.TeleBot(API_TOKEN)


def get_currency_base():
    resp = req.get('https://www.cbr-xml-daily.ru/daily_json.js').json()
    date = datetime.fromisoformat(resp['Timestamp']).strftime('%d/%m/%y %H:%M')
    cur = f'Курсы валют на {date}\n\n'
    cur += f"\U0001F1FA\U0001F1F8 Доллар США: {resp['Valute']['USD']['Value']} ₽\n"
    cur += f"\U0001F1EA\U0001F1FA Евро: {resp['Valute']['EUR']['Value']} ₽\n"
    cur += f"\U0001F1E8\U0001F1F3 Китайский юань: {resp['Valute']['CNY']['Value']} ₽"
    return cur


@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, 'Hi, I am bot')


@bot.message_handler(func=lambda message: True)
def echo_message(message):
    bot.reply_to(message, get_currency_base())


bot.infinity_polling()
