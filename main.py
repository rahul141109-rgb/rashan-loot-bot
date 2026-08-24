from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Put your Telegram Bot Token here
BOT_TOKEN = "8705161396:AAFGmx-A85oAXKnnzla-7DEE-7qJ1qpaZqs"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Welcome to Rashan Loots Bot! 👋\n\n"
        "Send your message or screenshot here."
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Messages are received here.
    # You can add your own reply logic later.
    await update.message.reply_text(
        "Message received ✅"
    )


def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(
        filters.TEXT | filters.PHOTO,
        handle_message
    ))

    print("Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
