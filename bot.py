import os
import re
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

user_text = {}  # har user ka last set text

# 🔹 Sirf NORMAL text (caption nahi)
async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.caption:   # agar caption hai to ignore
        return

    chat_id = update.message.chat_id
    text = update.message.text.strip()

    user_text[chat_id] = text
    await update.message.reply_text("✅ Text set successfully")

# 🔹 Video handler
async def video_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    caption = update.message.caption or ""

    replace_with = user_text.get(chat_id, "@BHAI_EDITS")

    # "Extracted By :" ke baad ka text replace
    new_caption = re.sub(
        r"(Extracted By\s*:\s*).*",
        r"\1" + replace_with,
        caption,
        flags=re.IGNORECASE
    )

    await context.bot.copy_message(
        chat_id=chat_id,
        from_chat_id=chat_id,
        message_id=update.message.message_id,
        caption=new_caption
    )

def main():
    # 🔐 TOKEN ENV se lena (Railway ke liye)
    TOKEN = os.getenv("BOT_TOKEN")

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))
    app.add_handler(MessageHandler(filters.VIDEO, video_handler))

    print("🤖 Bot started successfully...")
    app.run_polling()

if __name__ == "__main__":
    main()
