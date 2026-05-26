import telebot
import json
import os
from datetime import datetime

# Render'da "Environment" kısmına TOKEN adında değişken eklemeyi unutma
TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(TOKEN)

DOSYA = "stok.json" 

default_stok = {
    "Jack Daniels 1L": {"adet": 12, "kritik": 3},
    "Chivas Regal 12": {"adet": 8, "kritik": 2},
    "Grey Goose": {"adet": 5, "kritik": 2},
    "Johnnie Walker Black": {"adet": 10, "kritik": 3},
    "Absolut Vodka": {"adet": 15, "kritik": 4},
}

SIFRE = "TheKeep54"  
yetkililer = {} 

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
def basla(message):
    user_id = message.from_user.id
    if str(user_id) in yetkililer:
        bot.reply_to(message, "✅ Hoş geldin! Bot aktif.\n\n/stok\n/rapor")
    else:
        bot.reply_to(message, "🔒 Bu bot sadece yetkili kişiler tarafından kullanılabilir.\n\nLütfen şifreyi giriniz:")

@bot.message_handler(func=lambda m: True)
def mesaj_isle(message):
    user_id = message.from_user.id
    text = message.text.strip()

    if str(user_id) not in yetkililer:
        if text == SIFRE:
            yetkililer[str(user_id)] = True
            bot.reply_to(message, "✅ Şifre doğru! Komutlar:\n/stok - Güncel durum\n/rapor - Liste\nÖrn: Jack Daniels +5")
        else:
            bot.reply_to(message, "❌ Yanlış şifre!")
        return

    try:
        if text.startswith('/stok'):
            stok = yukle_stok()
            metin = "📊 GÜNCEL STOK\n\n"
            for urun, veri in stok.items():
                durum = "⚠️" if veri["adet"] <= veri["kritik"] else "✅"
                metin += f"{durum} {urun}: {veri['adet']}\n"
            bot.reply_to(message, metin, parse_mode="Markdown")

        elif text.startswith('/rapor'):
            stok = yukle_stok()
            metin = f"📋 RAPOR ({datetime.now().strftime('%H:%M')})\n\n"
            for urun, veri in stok.items():
                metin += f"{urun}: {veri['adet']} (Kritik: {veri['kritik']})\n"
            bot.reply_to(message, metin, parse_mode="Markdown")

        elif "+" in text or "-" in text:
            islem = "+" if "+" in text else "-"
            parts = text.split(islem)
            urun = parts[0].strip()
            adet = int(parts[1].strip())

            stok = yukle_stok()
            if urun in stok:
                if islem == "+":
                    stok[urun]["adet"] += adet
                else:
                    stok[urun]["adet"] = max(0, stok[urun]["adet"] - adet)
                
                kaydet_stok(stok)
                bot.reply_to(message, f"✅ İşlem başarılı: {urun} -> {stok[urun]['adet']}")
            else:
                bot.reply_to(message, "❌ Ürün bulunamadı.")
    except:
        bot.reply_to(message, "❌ Hatalı komut formatı. Örn: 'Jack Daniels +5'")

if _name_ == "_main_":
    bot.infinity_polling(drop_pending_updates=True)
