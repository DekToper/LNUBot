import requests
import telebot
import datetime
import time

from googletrans import Translator
from time import gmtime, strftime

bot = telebot.TeleBot('888879793:AAHGWl7JtlXA_3Jbt9gTfLMTlDBVr44S68k')


def get_group_id(message):
    id = 0
    k = 1
    i = 0
    try:
        id = int(obj._group[4]) * 10 + int(obj._group[5])
    except IndexError:
        id = int(obj._group[0]) * 10 + int(obj._group[1])
    except AttributeError:
        bot.send_message(message.chat.id, "Ви ще не вказали свою групу.\nЩоб вказати свою групу введіть - /group")
        return 0
    return id


def send_schedule(message):
    group_id = get_group_id(message)
    day = int(datetime.datetime.today().weekday())
    if day != 5 != 6:
        way = 'C:/TeleBot/Schedule/' + str(group_id) + '/' + str(day) + '.png'
        bot.send_photo(message.chat.id, photo=open(way, 'rb'))


def get_group(message):
    obj._group = message.text.lower()
    bot.send_message(message.chat.id, "Твоя група - " + message.text.upper())
    return True


def obj():
    _group: str = " "


def get_wea(message):
    r = requests.get("https://api.darksky.net/forecast/7deae5a2bf56ae2f94ee4180065a0c21/49.8409716,24.0142935")
    res: object = r.json()
    city = "Львові"
    x = res['currently']

    message_s = "Стан погоди: "
    _summ = x['summary']
    trans = Translator()
    s = trans.translate(_summ, dest='uk', src='en').text

    message_p = "Інтенсивність осаду: "
    p = x['precipIntensity']

    message_speed = "Швидкість вітру: "
    wspeed = x['windSpeed']

    tmp: str = (x['temperature'])
    message_t = "Температура: "
    tmp: int = (x['temperature'] - 32) / 2
    tmp = tmp + tmp / 10
    bot.send_message(message.chat.id, "Погода в" + city + "\n" +
                     message_s + s + "\n" +
                     message_t + str(round(tmp, 1)) + " С°\n" +
                     message_speed + str(wspeed) + " км/год.\n""" +
                     message_p + str(p) + " %")


@bot.message_handler(commands=['start'])
def start_message(message):
    name = message.from_user.first_name
    bot.send_message(message.chat.id, 'Привіт, ' + name + '.')
    bot.send_message(message.chat.id,
                     'Щоб отримувати розклад кожен день, вам потрібно вказати свою групу, за допомогою команди - /group')


@bot.message_handler(commands=['go'])
def get_schedule(message):
    while True:
        if int(datetime.datetime.today().weekday()) != 5 != 6:
            if int(strftime("%H", gmtime())) == 4:
                if int(strftime("%M", gmtime())) == 0:
                    if int(strftime("%S", gmtime())) == 0:
                        send_schedule(message)
            else:
                h = ((24 - int(strftime("%H", gmtime()))) + 4) * 3600
                m = (60 - int(strftime("%M", gmtime()))) * 60
                s = 60 - int(strftime("%S", gmtime()))
                time.sleep(h + m + s - 10)


@bot.message_handler(commands=['list'])
def start_message(message):
    bot.send_message(message.chat.id, 'Cписок доступних команд: /start , /list, /wea, /info, /group, /my_group')


@bot.message_handler(commands=['wea'])
def start_message(message):
    get_wea(message)


@bot.message_handler(commands=['info'])
def start_message(message):
    bot.send_message(message.chat.id, "Telegram Bot \"FUCT\" developed for students." +
                     "\nBy: DevTeam\n\n" +
                     "Доступні команди: " +
                     "\n/list - Перегляд доступних команд." +
                     "\n/info - Інформація про бота." +
                     "\n/start - Почати переписку з ботом." +
                     "\n/wea - Інформація про стан погоди у Львові." +
                     "\n/group - Встановити свою групу." +
                     "\n/my_group - Переглянути свою групу." +
                     "\n/go - Активувати надсилання розкладу." +
                     "\n/Schedule - Отримати розклад.")


@bot.message_handler(commands=['group'])
def start_message(message):
    bot.send_message(message.chat.id, "Вкажіть свою групу: ")
    bot.register_next_step_handler(message, get_group)


@bot.message_handler(commands=['my_group'])
def start_message(message):
    try:
        bot.send_message(message.chat.id,
                         "Твоя група: " + obj._group + "\nЩоб змінити\вказати свою групу введіть - /group")
    except AttributeError:
        bot.send_message(message.chat.id, "Ви ще не вказали свою групу.\nЩоб вказати свою групу введіть - /group")


@bot.message_handler(commands=['Schedule'])
def start_message(message):
    send_schedule(message)


bot.polling()
