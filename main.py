# from KeshaBot import KeshaBot
#
#
# keshaBot = KeshaBot;
# keshaBot.connect_to(self=KeshaBot,token="914475162:AAEqTvcLdEYLudu1sPwTfWNXeLC6oKFNNzE")
# keshaBot.sendEchoMessage(self=KeshaBot, message="Hello world")
from __future__ import unicode_literals

import mechanize
import openweathermapy.core as owm
import telebot
import youtube_dl
from mechanize import Browser
from telebot import types
import urllib.parse as urlparse
from urllib.parse import parse_qs
from dotenv import load_dotenv
import os

load_dotenv()


token = os.getenv('TOKEN')
appid = os.getenv('APPID')
bot = telebot.TeleBot(token)


settings = {"APPID": appid,"units": "metric", "lang": "RU"}





@bot.message_handler(commands=['start'], content_types=["text"])
def echo_all(message):
    bot.send_chat_action(message.chat.id, "typing")
    #bot.send_message(message, message.text)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True,row_width=3)
    itembtn1 = types.KeyboardButton(text='Погода')
    itembtn2 = types.KeyboardButton(text='Youtube')
    markup.add(itembtn1, itembtn2)
    bot.send_message(message.chat.id, "Выберите действие:", reply_markup=markup)

@bot.message_handler(content_types=["text"])
def check_btn(message):
    getMessage = message.text.strip().lower()

    if getMessage == "погода":
        data = owm.get_current("Кишинев", **settings)
        temp = data("main.temp")
        feels = data("main.feels_like")
        name = data("name")
        whether = data["weather"][0]["description"]

        print(data)
        bot.send_message(message.chat.id, "Температура воздуха в Кишиневе сейчас " + str(temp)
                         + " градусов\nЧувствуется как " + str(feels) + " градусов\n"+
                          "На улице " + whether)
    elif getMessage == "youtube":
        bot.send_message(message.chat.id, "Введите ссылку на видео и нажмите Enter: ")
    elif str(message.text.strip()).find("youtube.com") != -1:
        try:

            url = message.text.strip()
            br = Browser()
            br.open(url)
            title = br.title()
            print(title)
        except (mechanize.URLError,mechanize.HTTPError) as e:
            bot.send_message(message.chat.id, "Ошибка, нет такого ресурса")

        try:
            ydl_opts = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            }
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                bot.send_message(message.chat.id, "Подождите немного... Видео обрабатывается")
                print(url)
                destionation = ydl.download([url])
                parser = urlparse.urlparse(url)
                param = parse_qs(parser.query)['v']
                name = str(title).replace(" - YouTube", "-" + str(param).replace("['", "").replace("']", ""))
                audio = open(name + ".mp3", 'rb')
                bot.send_audio(message.chat.id, audio)
        except (youtube_dl.DownloadError,telebot.apihelper.ApiException):
            bot.send_message(message.chat.id, "Ошибка скачивания, неправильная ссылка либо слижком большой файл!")
        # else:
        #     bot.send_message(message.chat.id, "Неправильная ссылка")
    elif message.text.strip().lower() == "спасибо":
        bot.send_message(message.chat.id, "Это тебе спасибо:)")
    else:
        bot.send_message(message.chat.id, "Неправильная команда")

bot.polling()