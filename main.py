import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, Message
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    CallbackContext,
    filters
)

# توکن از محیط گرفته میشه (Zeabur Variable)
BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHANNEL_ID = "@EditNameh_IRAN"

# لاگ‌برداری
logging.basicConfig(level=logging.INFO)

# نقشه تبدیل به خط میخی
cuneiform_map = {
    "ا": "𒀀", "ب": "𒁀", "پ": "𒁁", "ت": "𒋾", "ث": "𒌨", "ج": "𒊩", "چ": "𒆜",
    "ح": "𒄩", "خ": "𒅗", "د": "𒁲", "ذ": "𒁺", "ر": "𒊑", "ز": "𒊓", "ژ": "𒆠",
    "س": "𒊬", "ش": "𒋛", "ص": "𒍑", "ض": "𒍣", "ط": "𒋾", "ظ": "𒌋", "ع": "𒀭",
    "غ": "𒐈", "ف": "𒅗", "ق": "𒆪", "ک": "𒆠", "گ": "𒐊", "ل": "𒇽", "م": "𒈬",
    "ن": "𒉡", "و": "𒉿", "ه": "𒄭", "ی": "𒅀", " ": "  "
}

def to_cuneiform(text: str) -> str:
    return ''.join(cuneiform_map.get(c, c) for c in text)

async def check_membership(user_id, context: ContextTypes.DEFAULT_TYPE) -> bool:
    try:
        member = await context.bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)
        return member.status in ["member", "creator", "administrator"]
    except:
        return False

async def start(update: Update, context: CallbackContext):
    user = update.effective_user
    if await check_membership(user.id, context):
        await update.message.reply_text("👋 خوش اومدی! متن فارسی بفرست تا برات به خط میخی تبدیلش کنم.")
    else:
        keyboard = [
            [InlineKeyboardButton("📢 عضویت در کانال", url="https://t.me/EditNameh_IRAN")],
            [InlineKeyboardButton("✅ عضو شدم", callback_data="joined")]
        ]
        await update.message.reply_text("برای استفاده از ربات، اول باید عضو کانال بشی:", reply_markup=InlineKeyboardMarkup(keyboard))

async def handle_private_message(update: Update, context: CallbackContext):
    user = update.effective_user
    if await check_membership(user.id, context):
        converted = to_cuneiform(update.message.text)
        await update.message.reply_text(f"🪶 متن شما به خط میخی:\n\n{converted}")
    else:
        await start(update, context)

async def convert_group_reply(update: Update, context: CallbackContext):
    if update.message.reply_to_message and update.message.text.startswith("تبدیل به میخی"):
        original: Message = update.message.reply_to_message
        converted = to_cuneiform(original.text)
        await update.message.reply_text(f"🪶 تبدیل:\n\n{converted}")

# راه‌اندازی برنامه
app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & filters.ChatType.PRIVATE, handle_private_message))
app.add_handler(MessageHandler(filters.TEXT & filters.ChatType.GROUPS, convert_group_reply))

if __name__ == "__main__":
    app.run_polling()
