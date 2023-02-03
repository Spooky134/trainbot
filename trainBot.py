import telebot
from auth_data import token
from parse import get_trains_info
from telebot import types

city_from = 'Минск'
city_to = ''
date = '2022-08-27'


# trains = None
# target_train = None

def telegram_bot(tk):
    bot = telebot.TeleBot(tk)

    @bot.message_handler(commands=["start"])
    def start(message):
        bot.send_message(message.from_user.id, 'Hello passenger')

    @bot.message_handler(content_types=["text"])
    def get_message(message):
        if message.text == '/trains':
            bot.send_message(message.from_user.id, 'Откуда едем?')
            bot.register_next_step_handler(message, get_city_from)
        else:
            bot.send_message(message.from_user.id, 'Напиши /trains')

    def get_city_from(message):
        global city_from
        city_from = message.text
        bot.send_message(message.from_user.id, 'Куда едем?')
        bot.register_next_step_handler(message, get_city_to)

    def get_city_to(message):
        global city_to
        city_to = message.text
        bot.send_message(message.from_user.id, 'Когда едем?')
        bot.register_next_step_handler(message, get_date)

    def get_date(message):
        global date
        date = message.text
        bot.send_message(message.from_user.id, 'Секундочку...')
        trains, url = get_trains_info(city_from=city_from, city_to=city_to, date=date)
        for train in trains:
            mes = f'{train.link}\n{train.train_type}\n{train.number} {train.train_route}\n{train.city_from}' \
                  f' ({train.departure}) --> {train.city_to} ({train.arrival})\nВремя в пути: {train.travel_time}\n'
            for places in train.places:
                mes += f'Тип:{places[0]}  Количество:{places[1]}  Цена:{places[2]}\n'
            bot.send_message(message.from_user.id, mes)

    bot.polling()


if __name__ == '__main__':
    telegram_bot(token)
