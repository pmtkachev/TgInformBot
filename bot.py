from threading import Thread
from time import sleep

import schedule
import telebot

import parse_func as ps
from const import API_TOKEN, CHAT_ID

bot = telebot.TeleBot(API_TOKEN)


def schedule_checker():
    while True:
        schedule.run_pending()
        sleep(2)


def daily_notif():
    message_string = ps.get_currency_base() + '\n\n' + ps.get_weather('Подольск') + \
                     '\n\n' + ps.get_quote()
    return bot.send_message(CHAT_ID, message_string)


if __name__ == '__main__':
    schedule.every().day.at('04:35').do(daily_notif)
    Thread(target=schedule_checker, daemon=True).start()


    @bot.message_handler(commands=['start'])
    def send_welcome(message):
        bot.send_message(message.chat.id, 'Привет! Это бот-информатор.\n'
                                          'Он присылает сообщение каждый день в одно и тоже время.\n'
                                          'Содержание сообщения и время определяет пользователь.')


    bot.infinity_polling()
