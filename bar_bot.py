import telebot
import json
import os

TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Bot çalışıyor ve seni duyuyorum!")

@bot.message_handler(func=lambda m: True)
def echo_all(message):
    bot.reply_to(message, "Mesajını aldım: " + message.text)

bot.infinity_polling()
