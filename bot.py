import telebot
from telebot import types
import requests

bot = telebot.TeleBot('1625581742:AAE3xsoGvlQ7xtKNqZF3hWQnLOO1_dxVTk0')

status = {}
nicks = {}
doctors = {}
times = {}

markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
itembtn1 = types.KeyboardButton('Никифорова Елизавета Юрьевна')
itembtn2 = types.KeyboardButton('Анотьева Ирина Михайловна')
markup.add(itembtn1, itembtn2)

markupt = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
markupt.add(types.KeyboardButton('18:00'), types.KeyboardButton('19:00'), types.KeyboardButton('20:00'), types.KeyboardButton('21:00'), types.KeyboardButton("22:00"))

markupb = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
markupb.add(types.KeyboardButton("/reg"))

def send_request(user_id):
    global nicks, doctors, times
    r = requests.post('https://easydoctorr.herokuapp.com/telegramrecord/', data={'username': nicks[user_id], 'doctor': doctors[user_id], 'time': times[user_id]})
    return r.content

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, '👋Привет, я бот EasyDoctor.\nС помощью меня ты сможешь записаться к любому врачу!\n\nЧтобы записаться к доктору воспользуйтесь командой /reg')
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
        bot.send_message(message.chat.id, 'К какому доктору вы хотите записаться?', reply_markup=markup)
        status[message.chat.id] = 'doctor_waiting'
    elif status[message.chat.id] == 'doctor_waiting':
        if message.text not in ['Анотьева Ирина Михайловна', 'Никифорова Елизавета Юрьевна']:
            bot.send_message(message.chat.id, 'Данного доктора нет в нашей системе')
            return 1
        doctors[message.chat.id] = message.text
        bot.send_message(message.chat.id, 'Пришлите время на которое вы хотите записаться', reply_markup=markupt)
        status[message.chat.id] = 'time_waiting'
    elif status[message.chat.id] == 'time_waiting':
        times[message.chat.id] = message.text
        s = send_request(message.chat.id)
        bot.send_message(message.chat.id, str(s), reply_markup=markupb)
        if s:
            bot.send_message(message.chat.id, '📝Спасибо! Ваша заявка успешно подана.', reply_markup=markupb)
        else:
            bot.send_message(message.chat.id, '❌Отмена! Запись к данному доктору на данное время уже существует!', reply_markup=markupb)
        status[message.chat.id] = 'main'
    else:
        bot.send_message(message.chat.id, '💡Чтобы записаться к доктору воспользуйтесь командой /reg')

bot.polling()
