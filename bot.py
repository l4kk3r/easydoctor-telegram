import telebot
import requests

bot = telebot.TeleBot('1625581742:AAE3xsoGvlQ7xtKNqZF3hWQnLOO1_dxVTk0')

status = {}
nicks = {}
doctors = {}
times = {}


def send_request(user_id):
    global nicks, doctors, times
    requests.post('https://easydoctorr.herokuapp.com/telegramrecord/', data={'username': nicks[user_id], 'doctor': doctors[user_id], 'time': times[user_id]})


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, '👋Привет, я бот EasyDoctor.\nС помощью меня ты сможешь записаться к любому врачу!')
    status[message.chat.id] = 'main'

@bot.message_handler(commands=['reg'])
def start_message(message):
    bot.send_message(message.chat.id, 'Пришлите свой никнейм в нашей системе')
    status[message.chat.id] = 'name_waiting'

@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.chat.id not in status:
        status[message.chat.id] = 'main'
    
    if status[message.chat.id] == 'name_waiting':
        nicks[message.chat.id] = message.text
        bot.send_message(message.chat.id, 'Пришлите ФИО доктора к которому вы хотите записаться')
        status[message.chat.id] = 'doctor_waiting'
    elif status[message.chat.id] == 'doctor_waiting':
        doctors[message.chat.id] = message.text
        bot.send_message(message.chat.id, 'Пришлите время на которое вы хотите записаться')
        status[message.chat.id] = 'time_waiting'
    elif status[message.chat.id] == 'time_waiting':
        times[message.chat.id] = message.text
        send_request(message.chat.id)
        bot.send_message(message.chat.id, 'Спасибо! Ваша заявка успешно подана.')
        status[message.chat.id] = 'main'
    else:
        bot.send_message(message.chat.id, 'Чтобы зарегистрироваться к доктору воспользуйтесь командой /reg')

bot.polling()