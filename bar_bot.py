import telebot
import json
import os

TOKEN = "8641761191:AAG20Xs8C7yLGb0Kb8La2TCVASFi0PoPK9U"
bot = telebot.TeleBot(TOKEN)

# Bu liste geçici olarak hafızada tutulacak (Render'da en güvenli yöntem budur)
stok = {
    "Jack Daniels 1L": 12,
    "Chivas Regal 12": 8,
    "Grey Goose": 5,
    "Johnnie Walker Black": 10
}

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Bot aktif! /stok yazarak listeyi görebilirsin.")

@bot.message_handler(func=lambda m: True)
def mesaj(message):
    text = message.text.strip()
    if text == "/stok":
        cevap = "📊 STOKLAR:\n\n"
        for urun, adet in stok.items():
            cevap += f"{urun}: {adet}\n"
        bot.reply_to(message, cevap)
    else:
        bot.reply_to(message, "Komut anlaşılamadı. /stok yazabilirsin.")

bot.infinity_polling()
