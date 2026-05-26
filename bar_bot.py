import telebot
import json
from datetime import datetime

TOKEN = "8641761191:AAG20Xs8C7yLGb0Kb8La2TCVASFi0PoPK9U"  # Kendi token'in

bot = telebot.TeleBot(TOKEN)

DOSYA = "stok.json"
KULLANICILAR_DOSYA = "yetkililer.json"

SIFRE = "TheKeep54"   # 
default_stok = {
    "Jack Daniels 1L": {"adet": 12, "kritik": 3},
    "Chivas Regal 12": {"adet": 8, "kritik": 2},
    "Grey Goose": {"adet": 5, "kritik": 2},
    "Johnnie Walker Black": {"adet": 10, "kritik": 3},
    "Absolut Vodka": {"adet": 15, "kritik": 4},
}

yetkililer = {}  # Kullanıcı ID'leri burada tutulacak

def yukle_stok():
    try:
        with open(DOSYA, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        with open(DOSYA, "w", encoding="utf-8") as f:
            json.dump(default_stok, f, ensure_ascii=False, indent=2)
        return default_stok

def kaydet_stok(stok):
    with open(DOSYA, "w", encoding="utf-8") as f:
        json.dump(stok, f, ensure_ascii=False, indent=2)

def yetkili_mi(user_id):
    return str(user_id) in yetkililer

@bot.message_handler(commands=['start'])
def basla(message):
    user_id = message.from_user.id
    if yetkili_mi(user_id):
        bot.reply_to(message, "✅ Hoş geldin! Bot aktif.\n\n/stok\n/rapor")
    else:
        bot.reply_to(message, "🔒 Bu bot sadece yetkili kişiler tarafından kullanılabilir.\n\nŞifreyi giriniz:")

@bot.message_handler(func=lambda m: True)
def mesaj_isle(message):
    user_id = message.from_user.id
    text = message.text.strip()

    # Şifre kontrolü
    if not yetkili_mi(user_id):
        if text == SIFRE:
            yetkililer[str(user_id)] = True
            bot.reply_to(message, "✅ Şifre doğru! Artık botu kullanabilirsiniz.\n\nKomutlar:\n/stok → Güncel stok\n/rapor → Detaylı rapor\nÜrün -3 → Eksilt\nÜrün +5 → Ekle")
        else:
            bot.reply_to(message, "❌ Yanlış şifre!")
        return

    # Yetkili ise normal komutlar
    try:
        if text.startswith('/stok'):
            # ... (önceki stok kodunu buraya koy)
            stok = yukle_stok()
            metin = "📊 *GÜNCEL STOK*\n\n"
            for urun, veri in stok.items():
                if veri["adet"] <= veri["kritik"]:
                    metin += f"⚠️ {urun}: *{veri['adet']}*\n"
                else:
                    metin += f"✅ {urun}: {veri['adet']}\n"
            bot.reply_to(message, metin, parse_mode="Markdown")

        elif text.startswith('/rapor'):
            # rapor kodu...
            stok = yukle_stok()
            metin = f"📋 *DETAYLI RAPOR* - {datetime.now().strftime('%d.%m.%Y %H:%M')}\n\n"
            for urun, veri in stok.items():
                metin += f"{urun}: {veri['adet']} adet (Kritik: {veri['kritik']})\n"
            bot.reply_to(message, metin)

        elif "+" in text or "-" in text:
            # Eksilt/Ekle kodu (önceki kodun aynı)
            if "+" in text:
                urun, adet_str = [x.strip() for x in text.split("+", 1)]
                adet = int(adet_str)
                islem = "eklendi"
            else:
                urun, adet_str = [x.strip() for x in text.split("-", 1)]
                adet = int(adet_str)
                islem = "eksiltildi"

            stok = yukle_stok()
            if urun in stok:
                if islem == "eklendi":
                    stok[urun]["adet"] += adet
                else:
                    stok[urun]["adet"] -= adet
                    if stok[urun]["adet"] < 0:
                        stok[urun]["adet"] = 0
                kaydet_stok(stok)
                bot.reply_to(message, f"✅ {adet} adet {urun} {islem}.")
                if stok[urun]["adet"] <= stok[urun]["kritik"]:
                    bot.reply_to(message, f"⚠️ KRİTİK! {urun} sadece {stok[urun]['adet']} kaldı.")
            else:
                bot.reply_to(message, "❌ Bu ürün stokta yok.")
    except:
        bot.reply_to(message, "❌ Komut formatı hatalı.")

print("Bot çalışıyor (Şifre korumalı)...")
bot.infinity_polling()
