import telebot
import os

# TOKEN'ını buraya tırnakların arasına yapıştır
TOKEN = "8641761191:AAG20Xs8C7yLGb0Kb8La2TCVASFi0PoPK9U"
bot = telebot.TeleBot(TOKEN)

# Stok listesi (Kodun içine gömülü)
stok = {
    "Jack Daniels 1L": 12,
    "Chivas Regal 12": 8,
    "Grey Goose": 5,
    "Johnnie Walker Black": 10
}

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Bot aktif! Stokları görmek için /stok yaz.")

@bot.message_handler(commands=['stok'])
def show_stock(message):
    cevap = "📊 CURRENT STOCK:\n\n"
    for item, count in stok.items():
        cevap += f"{item}: {count}\n"
    bot.reply_to(message, cevap)

@bot.message_handler(func=lambda m: True)
def unknown(message):
    bot.reply_to(message, "Sadece /stok komutunu kullanabilirsin.")

print("Bot çalışmaya başladı...")
bot.infinity_polling()
