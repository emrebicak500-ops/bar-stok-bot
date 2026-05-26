import telebot
import json
import os

# Telegram bot tokenin (Buraya senin uzun kodunu yapıştır)
TOKEN = "8641761191:AAG20Xs8C7yLGb0Kb8La2TCVASFi0PoPK9U"
bot = telebot.TeleBot(TOKEN)

# Stok bilgilerinin tutulacağı dosya ismi
DOSYA = "stok.json"

# Varsayılan stok listesi (Bot ilk açıldığında boşsa bunu kullanır)
default_stok = {
    "Jack Daniels 1L": {"adet": 12},
    "Chivas Regal 12": {"adet": 8},
    "Grey Goose": {"adet": 5},
    "Johnnie Walker Black": {"adet": 10}
}

def yukle_stok():
    if not os.path.exists(DOSYA):
        with open(DOSYA, "w", encoding="utf-8") as f:
            json.dump(default_stok, f, ensure_ascii=False, indent=2)
        return default_stok
    with open(DOSYA, "r", encoding="utf-8") as f:
        return json.load(f)

def kaydet_stok(stok):
    with open(DOSYA, "w", encoding="utf-8") as f:
        json.dump(stok, f, ensure_ascii=False, indent=2)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Merhaba! Stokları görmek için /stok yazabilirsin.")

@bot.message_handler(func=lambda m: True)
def mesaj_isle(message):
    text = message.text.strip()
    
    if text.startswith('/stok'):
        stok = yukle_stok()
        cevap = "📊 STOK DURUMU:\n\n"
        for urun, veri in stok.items():
            cevap += f"{urun}: {veri['adet']}\n"
        bot.reply_to(message, cevap)
    
    # Basit bir ekleme mantığı (örneğin: Jack Daniels 1L+2)
    elif "+" in text:
        try:
            urun, adet = text.split("+")
            stok = yukle_stok()
            if urun in stok:
                stok[urun]["adet"] += int(adet)
                kaydet_stok(stok)
                bot.reply_to(message, f"✅ Güncellendi: {urun} yeni stok {stok[urun]['adet']}")
        except:
            bot.reply_to(message, "Hata! Format: UrunIsmi+Adet")

bot.infinity_polling()
