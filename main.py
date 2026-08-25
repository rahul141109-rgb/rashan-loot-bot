from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = "8705161396:AAFGmx-A85oAXKnnzla-7DEE-7qJ1qpaZqs"
ADMIN_CHAT_ID = 8143010503

# User chat IDs
user_chats = {}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Welcome to Rashan Loots Bot! 👋\n\n"
        "Send your message or screenshot here."
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat_id = update.effective_chat.id

    # Save user's chat ID
    user_chats[user.id] = chat_id

    # Confirmation to user
    await update.message.reply_text("Message received ✅")

    username = f"@{user.username}" if user.username else "No username"

    # Send text message to admin
    if update.message.text:
        await context.bot.send_message(
            chat_id=ADMIN_CHAT_ID,
            text=(
                "📩 New Message\n\n"
                f"👤 Name: {user.first_name}\n"
                f"🔹 Username: {username}\n"
                f"🆔 User ID: {user.id}\n\n"
                f"💬 Message:\n{update.message.text}\n\n"
                f"📌 Reply command:\n"
                f"/reply {user.id} Your message"
            )
        )

    # Send screenshot to admin
    elif update.message.photo:
        await context.bot.send_photo(
            chat_id=ADMIN_CHAT_ID,
            photo=update.message.photo[-1].file_id,
            caption=(
                "📸 New Screenshot\n\n"
                f"👤 Name: {user.first_name}\n"
                f"🔹 Username: {username}\n"
                f"🆔 User ID: {user.id}\n\n"
                f"📌 Reply command:\n"
                f"/reply {user.id} Your message"
            )
        )


async def reply_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Only admin can use /reply
    if update.effective_chat.id != ADMIN_CHAT_ID:
        return

    if len(context.args) < 2:
        await update.message.reply_text(
            "Use:\n/reply USER_ID Your message"
        )
        return

    try:
        user_id = int(context.args[0])
    except ValueError:
        await update.message.reply_text("❌ Invalid User ID.")
        return

    message = " ".join(context.args[1:])

    if user_id not in user_chats:
        await update.message.reply_text(
            "❌ User chat not found. Ask the user to message the bot again."
        )
        return

    await context.bot.send_message(
        chat_id=user_chats[user_id],
        text=f"📩 Admin Reply:\n\n{message}"
    )

    await update.message.reply_text("✅ Reply sent.")


def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("reply", reply_user))

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
