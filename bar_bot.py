import telebot
import json
from datetime import datetime

TOKEN = "8641761191:AAG20Xs8C7yLGb0Kb8La2TCVASFi0PoPK9U"
bot = telebot.TeleBot(TOKEN)

DOSYA = "stok.json"

# İlk stoklar (istediğin gibi değiştir)
default_stok = {
    "Jack Daniels 1L": {"adet": 12, "kritik": 3},
    "Chivas Regal 12": {"adet": 8, "kritik": 2},
    "Grey Goose": {"adet": 5, "kritik": 2},
    "Johnnie Walker Black": {"adet": 10, "kritik": 3},
    "Absolut Vodka": {"adet": 15, "kritik": 4},
}

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

@bot.message_handler(commands=['start', 'help'])
def basla(message):
    bot.reply_to(message, 
        "🍻 Bar Stok Botu'na hoş geldin!\n\n"
        "Kullanım:\n"
        "• Ürün Adı -3   → Eksilt\n"
        "• Ürün Adı +5   → Ekle\n"
        "• /stok         → Güncel stok\n"
        "• /rapor        → Detaylı rapor")

@bot.message_handler(commands=['stok'])
def goster_stok(message):
    stok = yukle_stok()
    metin = "📊 *GÜNCEL STOK*\n\n"
    for urun, veri in stok.items():
        adet = veri["adet"]
        kritik = veri["kritik"]
        if adet <= kritik:
            metin += f"⚠️ {urun}: *{adet}* (Kritik!)\n"
        else:
            metin += f"✅ {urun}: {adet}\n"
    bot.reply_to(message, metin, parse_mode="Markdown")

@bot.message_handler(commands=['rapor'])
def detay_rapor(message):
    stok = yukle_stok()
    metin = f"📋 *DETAYLI RAPOR* - {datetime.now().strftime('%d.%m.%Y %H:%M')}\n\n"
    for urun, veri in stok.items():
        metin += f"{urun}: {veri['adet']} adet (Kritik: {veri['kritik']})\n"
    bot.reply_to(message, metin)

@bot.message_handler(func=lambda m: True)
def mesaj_isle(message):
    try:
        text = message.text.strip()
        stok = yukle_stok()
        
        # + veya - var mı kontrol et
        if " +" in text or " -" in text or text.count("+") == 1 or text.count("-") == 1:
            # Basit parsing
            if "+" in text:
                urun, adet_str = text.split("+", 1)
                adet = int(adet_str.strip())
                islem = "eklendi"
            else:
                urun, adet_str = text.split("-", 1)
                adet = int(adet_str.strip())
                islem = "eksiltildi"
            
            urun = urun.strip()
            
            if urun in stok:
                if islem == "eklendi":
                    stok[urun]["adet"] += adet
                else:
                    stok[urun]["adet"] -= adet
                    if stok[urun]["adet"] < 0:
                        stok[urun]["adet"] = 0
                
                kaydet_stok(stok)
                bot.reply_to(message, f"✅ *{adet} adet* {urun} {islem}.")
                
                # Kritik kontrol
                if stok[urun]["adet"] <= stok[urun]["kritik"]:
                    bot.reply_to(message, f"⚠️ DİKKAT! {urun} kritik seviyede ({stok[urun]['adet']} kaldı)")
            else:
                bot.reply_to(message, "❌ Bu ürün stokta yok. Önce eklemen lazım.")
        else:
            bot.reply_to(message, "❓ Anlamadım. Örnek: Jack Daniels -2 veya /stok yaz.")
            
    except:
        bot.reply_to(message, "❌ Hatalı format. Örnek kullanım:\nJack Daniels -3")

print("Bot çalışıyor...")
bot.infinity_polling()
