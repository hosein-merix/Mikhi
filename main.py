from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, CallbackContext
import os
import logging

BOT_TOKEN = os.environ.get("8040385853:AAFr9KQHLay0aR06Zvp2xl2Jj7Yvn7xJSY0")
CHANNEL_ID = "@EditNameh_IRAN"

logging.basicConfig(level=logging.INFO)

cuneiform_map = {
    "ا": "𒀀", "ب": "𒁀", "پ": "𒁁", "ت": "𒋾", "ث": "𒌨", "ج": "𒊩", "چ": "𒆜",
    "ح": "𒄩", "خ": "𒅗", "د": "𒁲", "ذ": "𒁺", "ر": "𒊑", "ز": "𒊓", "ژ": "𒆠",
    "س": "𒊬", "ش": "𒋛", "ص": "𒍑", "ض": "𒍣", "ط": "𒋾", "ظ": "𒌋", "ع": "𒀭",
    "غ": "𒐈", "ف": "𒅗", "ق": "𒆪", "ک": "𒆠", "گ": "𒐊", "ل": "𒇽", "م": "𒈬",
    "ن": "𒉡", "و": "𒉿", "ه": "𒄭", "ی": "𒅀", " ": "  "
}

def to_cuneiform(text):
    return ''.join(cuneiform_map.get(char, char) for char in text)

async def start(update: Update, context: CallbackContext):
    user = update.effective_user
    chat_member = await context.bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user.id)
    if chat_member.status in ['member', 'creator', 'administrator']:
        await update.message.reply_text("👋 خوش اومدی! متن فارسی بفرست تا برات به خط میخی تبدیلش کنم.")
    else:
        keyboard = [
            [InlineKeyboardButton("📢 عضویت در کانال", url="https://t.me/EditNameh_IRAN")],
            [InlineKeyboardButton("✅ عضو شدم", callback_data="joined")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("برای استفاده از ربات، اول باید عضو کانال بشی:", reply_markup=reply_markup)

async def handle_message(update: Update, context: CallbackContext):
    user = update.effective_user
    chat_member = await context.bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user.id)
    if chat_member.status in ['member', 'creator', 'administrator']:
        converted = to_cuneiform(update.message.text)
        await update.message.reply_text(f"🪶 متن شما به خط میخی:\n\n{converted}")
    else:
        await start(update, context)

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

if __name__ == "__main__":
    app.run_polling()
