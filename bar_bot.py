import sqlite3
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)

TOKEN = "8641761191:AAG20Xs8C7yLGb0Kb8La2TCVASFi0PoPK9U"

ADMIN_IDS = [123456789]  # kendi telegram id

# DATABASE
conn = sqlite3.connect("stok.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE,
    stock INTEGER
)
""")

conn.commit()


# START
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = """
🍺 Bar Stok Takip Botu

Komutlar:

/urunekle isim miktar
/stok isim
/satis isim miktar
/guncelle isim miktar
/liste
"""
    await update.message.reply_text(text)


# ADMIN CHECK
def is_admin(user_id):
    return user_id in ADMIN_IDS


# ÜRÜN EKLE
async def urunekle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        return await update.message.reply_text("Yetkisiz erişim!")

    try:
        name = context.args[0]
        stock = int(context.args[1])

        cursor.execute(
            "INSERT INTO products (name, stock) VALUES (?, ?)",
            (name, stock)
        )
        conn.commit()

        await update.message.reply_text(
            f"✅ {name} eklendi.\nStok: {stock}"
        )

    except sqlite3.IntegrityError:
        await update.message.reply_text("Bu ürün zaten mevcut.")

    except:
        await update.message.reply_text(
            "Kullanım:\n/urunekle kola 50"
        )


# STOK GÖR
async def stok(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        name = context.args[0]

        cursor.execute(
            "SELECT stock FROM products WHERE name=?",
            (name,)
        )

        result = cursor.fetchone()

        if result:
            await update.message.reply_text(
                f"📦 {name} stok: {result[0]}"
            )
        else:
            await update.message.reply_text("Ürün bulunamadı.")

    except:
        await update.message.reply_text(
            "Kullanım:\n/stok kola"
        )


# SATIŞ
async def satis(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        return await update.message.reply_text("Yetkisiz erişim!")

    try:
        name = context.args[0]
        amount = int(context.args[1])

        cursor.execute(
            "SELECT stock FROM products WHERE name=?",
            (name,)
        )

        result = cursor.fetchone()

        if not result:
            return await update.message.reply_text(
                "Ürün bulunamadı."
            )

        current_stock = result[0]

        if current_stock < amount:
            return await update.message.reply_text(
                "Yetersiz stok!"
            )

        new_stock = current_stock - amount

        cursor.execute(
            "UPDATE products SET stock=? WHERE name=?",
            (new_stock, name)
        )

        conn.commit()

        msg = f"🍻 {amount} adet {name} satıldı.\nYeni stok: {new_stock}"

        if new_stock <= 10:
            msg += "\n⚠️ KRİTİK STOK!"

        await update.message.reply_text(msg)

    except:
        await update.message.reply_text(
            "Kullanım:\n/satis kola 5"
        )


# STOK GÜNCELLE
async def guncelle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        return await update.message.reply_text("Yetkisiz erişim!")

    try:
        name = context.args[0]
        stock = int(context.args[1])

        cursor.execute(
            "UPDATE products SET stock=? WHERE name=?",
            (stock, name)
        )

        conn.commit()

        await update.message.reply_text(
            f"🔄 {name} yeni stok: {stock}"
        )

    except:
        await update.message.reply_text(
            "Kullanım:\n/guncelle kola 100"
        )


# LİSTE
async def liste(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cursor.execute("SELECT name, stock FROM products")

    products = cursor.fetchall()

    if not products:
        return await update.message.reply_text(
            "Ürün bulunamadı."
        )

    text = "📋 STOK LİSTESİ\n\n"

    for name, stock in products:
        icon = "🟢"

        if stock <= 10:
            icon = "🔴"

        text += f"{icon} {name} → {stock}\n"

    await update.message.reply_text(text)


# MAIN
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("urunekle", urunekle))
app.add_handler(CommandHandler("stok", stok))
app.add_handler(CommandHandler("satis", satis))
app.add_handler(CommandHandler("guncelle", guncelle))
app.add_handler(CommandHandler("liste", liste))

print("Bot çalışıyor...")
app.run_polling()
