from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Telegram Bot Token
BOT_TOKEN = "8705161396:AAFGmx-A85oAXKnnzla-7DEE-7qJ1qpaZqs"

# Your Telegram Chat ID
ADMIN_CHAT_ID = 8143010503


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Welcome to Rashan Loots Bot! 👋\n\n"
        "Send your message or screenshot here."
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Send confirmation to the user
    await update.message.reply_text("Message received ✅")

    user = update.effective_user
    username = f"@{user.username}" if user.username else "No username"

    # Forward text message to admin
    if update.message.text:
        await context.bot.send_message(
            chat_id=ADMIN_CHAT_ID,
            text=(
                "📩 New Message\n\n"
                f"👤 Name: {user.first_name}\n"
                f"🔹 Username: {username}\n"
                f"🆔 User ID: {user.id}\n\n"
                f"💬 Message:\n{update.message.text}"
            )
        )

    # Forward screenshot/photo to admin
    elif update.message.photo:
        await context.bot.send_photo(
            chat_id=ADMIN_CHAT_ID,
            photo=update.message.photo[-1].file_id,
            caption=(
                "📸 New Screenshot\n\n"
                f"👤 Name: {user.first_name}\n"
                f"🔹 Username: {username}\n"
                f"🆔 User ID: {user.id}"
            )
        )


def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    app.add_handler(
        MessageHandler(
            filters.TEXT | filters.PHOTO,
            handle_message
        )
    )

    print("Bot is running...")

    app.run_polling()


if __name__ == "__main__":
    main()
