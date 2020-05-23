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

settings = {"APPID": appid, "units": "metric", "lang": "EN"}


@bot.message_handler(commands=['start'], content_types=["text"])
def echo_all(message):
    bot.send_chat_action(message.chat.id, "typing")
    markup = types.ReplyKeyboardMarkup(row_width=2)
    itembtn1 = types.KeyboardButton(text='Whether')
    itembtn2 = types.KeyboardButton(text='Youtube')
    markup.add(itembtn1, itembtn2)
    bot.send_message(message.chat.id, "Chose command:", reply_markup=markup)


@bot.message_handler(content_types=["text"])
def check_btn(message):
    getMessage = message.text.strip().lower()

    if getMessage == "whether":
        data = owm.get_current("Chisinau", **settings)
        temp = data("main.temp")
        feels = data("main.feels_like")
        name = data("name")
        whether = data["weather"][0]["description"]

        print(data)
        bot.send_message(message.chat.id, "Air temperature in Chisinau is " + str(temp)
                         + " degree\nFeeling as " + str(feels) + " degree\n" +
                         "On outdoors is  " + whether)
    elif getMessage == "youtube":
        bot.send_message(message.chat.id, "Enter a Youtube video link and tap Enter key: ")
    elif str(message.text.strip()).find("youtube.com") != -1:
        try:

            url = message.text.strip()
            br = Browser()
            br.open(url)
            title = br.title()
            print(title)
        except (mechanize.URLError, mechanize.HTTPError) as e:
            bot.send_message(message.chat.id, "Error! Can`t get this resource!")

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
                bot.send_message(message.chat.id, "Wait a bit... Video is being processed")
                print(url)
                ydl.download([url])
                parser = urlparse.urlparse(url)
                param = parse_qs(parser.query)['v']
                name = str(title).replace(" - YouTube", "-" + str(param).replace("['", "").replace("']", ""))
                audio = open(name + ".mp3", 'rb')
                bot.send_audio(message.chat.id, audio)
        except (youtube_dl.DownloadError, telebot.apihelper.ApiException):
            bot.send_message(message.chat.id, "Error! This link is incorrect or this video is very large!")
    elif message.text.strip().lower() == "Thanks!":
        bot.send_message(message.chat.id, "Thanks you too:)")
    else:
        bot.send_message(message.chat.id, "Command is incorrect!")


bot.polling()
