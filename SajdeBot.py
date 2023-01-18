#!/usr/bin/env python3
import requests
import telebot
import datetime
from datetime import datetime
import json

TOKEN = '1061887785:AAH6qDqJ5RSowbSgF8MRyCd8kJ2IDqVydg8'
bot = telebot.TeleBot(TOKEN)

shirota = ''
dolgota = ''
x = datetime.now()
day = x.strftime("%x")
month = x.strftime("%m")
year = x.strftime("%Y")
URL = 'http://namaz.muftyat.kz/api/times/' + x.strftime("%Y")
#data = requests.get(URL)
keyboardcity = telebot.types.ReplyKeyboardMarkup(True, True)
keyboardcity.row('Алматы', 'Шымкент', 'Нұр-Сұлтан', "Тараз")

@bot.message_handler(commands = ['start'])
def start_command(message):
    a = message.from_user.first_name
    bot.send_message(message.chat.id, 'Добро пожаловать ' + a + '!')
    choosecity(message)
def getruss(cur):
    if(cur == "January"):
        return "Январь"
    if (cur == "February"):
        return "Февраль"
    if (cur == "March"):
        return "Март"
    if (cur == "April"):
        return "Апрель"
    if (cur == "May"):
        return "Май"
    if (cur == "June"):
        return "Июнь"
    if (cur == "July"):
        return "Июль"
    if (cur == "August"):
        return "Август"
    if (cur == "September"):
        return "Сентябрь"
    if (cur == "October"):
        return "Октябрь"
    if (cur == "November"):
        return "Ноябрь"
    if (cur == "December"):
        return "Декабрь"
def getsec(now):
    cur = int(int(now[7]) + int(now[6]) * 10)
    cur = cur + int((int(now[4]) + int(now[3]) * 10) * 60)
    cur = cur + int((int(now[1]) + int(now[0]) * 10) * 3600)
    return cur
def ostalosdo(now, slednamaz):
    slednamaz = slednamaz.replace(" ", "")
    slednamaz = slednamaz + ":00"
    cur = getsec(now)
    nex = getsec(slednamaz)
    ans = 0
    if(cur > nex):
        ans = nex + 86400 - cur
    else:
        ans = nex - cur
    return ans
def ostalosdostr(inter):
    chas = str(int(inter / 3600))
    ch = int(inter / 3600)
    if ch <= 9:
        chas = "0" + chas
    minutt = str(int((inter - int(inter / 3600) * 3600) / 60))
    mn = int((inter - int(inter / 3600) * 3600) / 60)
    if mn <= 9:
        minutt = "0" + minutt
    sec = str(int(inter - ch * 3600 - mn * 60))
    sc = int(inter - ch * 3600 - mn * 60)
    if sc <= 9:
        sec = "0" + sec
    return ("Осталось " + chas + ":" + minutt + ":" + sec + " до ")

keyboardback = telebot.types.ReplyKeyboardMarkup(True, True)
keyboardback.row("Назад", "Время")
def gettimes(shirota, dolgota):
    day_of_year = datetime.now().timetuple().tm_yday - 1  # day of the year

    data = requests.get(URL + '/' + shirota + '/' + dolgota).json()
    now = datetime.now()
    message = ''
    if(shirota == "43.238293" and dolgota == "76.945465"):
        message = 'Алматы'
    if (shirota == "42.3" and dolgota == '69.6'):
        message = 'Шымкент'
    if (shirota == "51.133333" and dolgota == "71.433333"):
        message = 'Нұр-Сұлтан'

    current_time = now.strftime("%X")
    month_in_words = getruss(x.strftime("%B"))
    answer = message + " " + x.strftime("%d") + " " + month_in_words + " " + x.strftime("%Y") + "\n\n"
    if (current_time > data['result'][day_of_year]['Isha'] or current_time < data['result'][day_of_year]['Fajr']):
        inter = ostalosdo(current_time, data['result'][day_of_year]['Fajr'])
        interst = ostalosdostr(inter)
        answer = answer + "Иша \n" + interst + "Фаджр"
    elif (current_time > data['result'][day_of_year]['Maghrib']):
        inter = ostalosdo(current_time, data['result'][day_of_year]['Isha'])
        interst = ostalosdostr(inter)
        answer = answer + "Магриб " + interst + "Иша"
    elif (current_time > data['result'][day_of_year]['Asr']):
        inter = ostalosdo(current_time, data['result'][day_of_year]['Maghrib'])
        interst = ostalosdostr(inter)
        answer = answer + "Аср " + interst + "Магриб"
    elif (current_time > data['result'][day_of_year]['Dhuhr']):
        inter = ostalosdo(current_time, data['result'][day_of_year]['Asr'])
        interst = ostalosdostr(inter)
        answer = answer + "Зухр " + interst + "Аср"
    elif (current_time > data['result'][day_of_year]['Sunrise']):
        inter = ostalosdo(current_time, data['result'][day_of_year]['Dhuhr'])
        interst = ostalosdostr(inter)
        answer = answer + "Восход " + interst + "Зухр"
    elif (current_time > data['result'][day_of_year]['Fajr']):
        inter = ostalosdo(current_time, data['result'][day_of_year]['Sunrise'])
        interst = ostalosdostr(inter)
        answer = answer + "Фаджр " + interst + "Восход"
    elif (current_time > data['result'][day_of_year]['Sunrise']):
        inter = ostalosdo(current_time, data['result'][day_of_year]['Fajr'])
        interst = ostalosdostr(inter)
        answer = answer + "Фаджр " + interst + "Восход"
    return answer

def choosecity(message):
    bot.send_message(message.chat.id, 'Выберите город в котором вы живете', reply_markup = keyboardcity)

@bot.message_handler(content_types = ['text'])
def prosot(message):
    if(message.text == 'Алматы' or message.text == 'Шымкент' or message.text == 'Нұр-Сұлтан'):
        send_text(message)
    else:
        back(message)

def send_text(message):
    global shirota, dolgota

    if message.text == 'Алматы':
        shirota = '43.238293'
        dolgota = '76.945465'

    if message.text == 'Шымкент':
        shirota = '42.3'
        dolgota = '69.6'

    if message.text == 'Нұр-Сұлтан':
        shirota = '51.133333'
        dolgota = '71.433333'

    answer = gettimes(shirota, dolgota)
    data = requests.get(URL + '/' + shirota + '/' + dolgota).json()
    now = datetime.now()
    day_of_year = datetime.now().timetuple().tm_yday - 1 # day of the year
    bot.send_message(message.chat.id, answer + "\n\nФаджр - " + data['result'][day_of_year]['Fajr'] + "\nВосход - " + data['result'][day_of_year]['Sunrise'] + "\nЗухр - "
                     + data['result'][day_of_year]['Dhuhr'] + "\nАср - " + data['result'][day_of_year]['Asr'] +
                     "\nМагриб - " + data['result'][day_of_year]['Maghrib'] + "\nИша - " + data['result'][day_of_year]['Isha'], reply_markup=keyboardback)

@bot.message_handler(content_types = ['text'])
def back(message):
    if message.text == "Назад":
        choosecity(message)
    else:
        send_text(message)


@bot.message_handler(commands = ['help'])
def help_command(message):
    bot.send_message(message.chat.id, 'Чтобы начать пользоваться ботом напишите /start')

#print(data.json())
bot.polling()