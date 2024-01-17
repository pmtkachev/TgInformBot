from datetime import timedelta, datetime

import requests
from bs4 import BeautifulSoup
from pyowm import OWM
from pyowm.utils.config import get_default_config

from const import OWM_TOKEN

owm = OWM(OWM_TOKEN)

config_dict = get_default_config()
config_dict['language'] = 'ru'

manager = owm.weather_manager()


def get_weather(city):
    observation = manager.weather_at_place(f'{city},RU')
    weather = observation.weather
    sunrise_time = (weather.sunrise_time(timeformat="date") + timedelta(hours=3)).strftime("%H:%M")
    sunset_time = (weather.sunset_time(timeformat="date") + timedelta(hours=3)).strftime("%H:%M")

    weather_string = f'Погода, {city}\n\n\U0001F321 Температура: {round(weather.temperature("celsius")["temp"])} °C, ' \
                     f'ощущается как {round(weather.temperature("celsius")["feels_like"])} °C.\n' \
                     f'🍃 Скорость ветра: {weather.wind()["speed"]} м/с\n' \
                     f'\U000026F1 {weather.detailed_status.capitalize()}.\n' \
                     f'\U0001F31E Восход: {sunrise_time}\n' \
                     f'\U0001F31C Закат: {sunset_time}'

    return weather_string


def get_currency_base():
    response = requests.get('https://www.cbr-xml-daily.ru/daily_json.js').json()
    date = datetime.fromisoformat(response['Timestamp']).strftime('%d/%m/%y %H:%M')

    currency_string = f'Курсы валют на {date}\n\n' \
                      f'\U0001F1FA\U0001F1F8 Доллар США: {response["Valute"]["USD"]["Value"]} ₽\n' \
                      f'\U0001F1EA\U0001F1FA Евро: {response["Valute"]["EUR"]["Value"]} ₽\n' \
                      f'\U0001F1E8\U0001F1F3 Китайский юань: {response["Valute"]["CNY"]["Value"]} ₽'

    return currency_string


def get_quote():
    resp = requests.get('https://citaty.info/random')
    bs_quote = BeautifulSoup(resp.text, 'html.parser')
    quote = f"\U0001F4D6 Цитата дня: {bs_quote.find('div', class_='field-item even last').text}"

    return quote
