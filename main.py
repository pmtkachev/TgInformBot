from datetime import datetime, timedelta

import requests as req
import telebot
from bs4 import BeautifulSoup
from pyowm import OWM
from pyowm.utils.config import get_default_config

API_TOKEN = ''
owm = OWM('')
config_dict = get_default_config()
config_dict['language'] = 'ru'
mgr = owm.weather_manager()

bot = telebot.TeleBot(API_TOKEN)


def get_currency_base():
    resp = req.get('https://www.cbr-xml-daily.ru/daily_json.js').json()
    date = datetime.fromisoformat(resp['Timestamp']).strftime('%d/%m/%y %H:%M')
    cur = f'Курсы валют на {date}\n\n'
    cur += f"\U0001F1FA\U0001F1F8 Доллар США: {resp['Valute']['USD']['Value']} ₽\n"
    cur += f"\U0001F1EA\U0001F1FA Евро: {resp['Valute']['EUR']['Value']} ₽\n"
    cur += f"\U0001F1E8\U0001F1F3 Китайский юань: {resp['Valute']['CNY']['Value']} ₽"
    return cur


def get_weather(city):
    observation = mgr.weather_at_place(f'{city},RU')
    weather = observation.weather
    weather_string = f'Погода, {city}\n\n\U0001F321 Температура: {round(weather.temperature("celsius")["temp"])} °C, ' \
                     f'ощущается как {round(weather.temperature("celsius")["feels_like"])} °C.\n' \
                     f'🍃 Скорость ветра: {weather.wind()["speed"]} м/с\n\U000026F1 {weather.detailed_status.capitalize()}.\n' \
                     f'\U0001F31E Восход: {(weather.sunrise_time(timeformat="date") + timedelta(hours=3)).strftime("%H:%M")}\n' \
                     f'\U0001F31C Закат: {(weather.sunset_time(timeformat="date") + timedelta(hours=3)).strftime("%H:%M")}'
    return weather_string


def get_quote():
    resp = req.get('https://citaty.info/random')
    bs = BeautifulSoup(resp.text, 'html.parser')
    quote = f"\U0001F4D6 Цитата дня: {bs.find('div', class_='field-item even last').text}"
    return quote


@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, 'Hi, I am bot')


@bot.message_handler(func=lambda message: True)
def echo_message(message):
    bot.send_message(message.chat.id, get_currency_base() + '\n\n' + get_weather('Подольск') +
                     '\n\n' + get_quote())


bot.infinity_polling()
