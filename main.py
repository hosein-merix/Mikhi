from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# مشخصات ربات
TOKEN = "8040385853:AAFr9KQHLay0aR06Zvp2xl2Jj7Yvn7xJSY0"
CHANNEL_ID = "@EditNameh_IRAN"  # آیدی کانال با @

# جدول تبدیل حروف فارسی به نمادهای خط میخی (نمونه‌ای)
cuneiform_map = {
    'ا': '𒀀', 'ب': '𒁀', 'پ': '𒁁', 'ت': '𒋾', 'ث': '𒊻', 'ج': '𒆜',
    'چ': '𒆝', 'ح': '𒄩', 'خ': '𒄷', 'د': '𒁲', 'ذ': '𒊑',
    'ر': '𒊒', 'ز': '𒍣', 'ژ': '𒆠', 'س': '𒊓', 'ش': '𒋗', 'ص': '𒍑',
    'ض': '𒍖', 'ط': '𒋫', 'ظ': '𒍣𒁍', 'ع': '𒀭', 'غ': '𒅗',
    'ف': '𒉺', 'ق': '𒆪', 'ک': '𒅗', 'گ': '𒄀', 'ل': '𒇽',
    'م': '𒈬', 'ن': '𒉡', 'و': '𒉿', 'ه': '𒄭', 'ی': '𒅀',
}

def to_cuneiform(text):
    return ''.join(cuneiform_map.get(ch, ch) for ch in text)

async def is_user_member(user_id, context):
    try:
        member = await context.bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)
        return member.status in ['member', 'administrator', 'creator']
    except:
        return False

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "سلام! 👋\nبه ربات خط میخی خوش اومدی.\nمتن فارسی‌تو بفرست تا به خط میخی برات تبدیل کنم. ✨"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    is_member = await is_user_member(user_id, context)

    if not is_member:
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("📢 عضویت در کانال", url="https://t.me/EditNameh_IRAN")]
        ])
        await update.message.reply_text(
            "🔒 برای استفاده از ربات باید اول عضو کانال بشی.\n👇 روی دکمه زیر بزن و بعد دوباره امتحان کن:",
            reply_markup=keyboard
        )
        return

    input_text = update.message.text
    output = to_cuneiform(input_text)

    pretty_message = f"""
📥 *متن شما:*
`{input_text}`

🔤 *تبدیل به خط میخی:*
`{output}`

📜 ربات *خط میخی*
    """
    await update.message.reply_text(pretty_message, parse_mode='Markdown')

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("✅ ربات راه‌اندازی شد.")
    app.run_polling()

if __name__ == '__main__':
    main()
