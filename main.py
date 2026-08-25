from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
    ContextTypes,
)

BOT_TOKEN = "8705161396:AAFGmx-A85oAXKnnzla-7DEE-7qJ1qpaZqs"
ADMIN_CHAT_ID = 8143010503


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Welcome to Rashan Loots Bot! 👋\n\n"
        "Send your message or screenshot here."
    )


async def handle_user_message(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    user_chat_id = update.effective_chat.id

    # Reply button — chat ID is stored internally in callback data
    keyboard = [
        [
            InlineKeyboardButton(
                "↩️ Reply",
                callback_data=f"reply:{user_chat_id}"
            )
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    # Send only the actual text to admin
    if update.message.text:
        await context.bot.send_message(
            chat_id=ADMIN_CHAT_ID,
            text=update.message.text,
            reply_markup=reply_markup
        )

    # Send screenshot/photo to admin
    elif update.message.photo:
        await context.bot.send_photo(
            chat_id=ADMIN_CHAT_ID,
            photo=update.message.photo[-1].file_id,
            reply_markup=reply_markup
        )


async def reply_button(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    query = update.callback_query

    # Only admin can use the Reply button
    if query.from_user.id != ADMIN_CHAT_ID:
        await query.answer(
            "❌ Not authorized.",
            show_alert=True
        )
        return

    await query.answer()

    user_chat_id = int(query.data.split(":")[1])

    # Store the chat ID internally
    context.user_data["reply_to_chat_id"] = user_chat_id

    await query.message.reply_text(
        "✍️ Reply type karke send karo.\n\n"
        "Tumhara next message seedha us bande ko chala jayega."
    )


async def send_admin_reply(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    # Only admin can send replies
    if update.effective_chat.id != ADMIN_CHAT_ID:
        return

    reply_to_chat_id = context.user_data.get("reply_to_chat_id")

    if not reply_to_chat_id:
        return

    # Don't treat commands as replies
    if update.message.text and update.message.text.startswith("/"):
        return

    # Send text reply to user
    if update.message.text:
        await context.bot.send_message(
            chat_id=reply_to_chat_id,
            text=update.message.text
        )

    # Send photo reply to user
    elif update.message.photo:
        await context.bot.send_photo(
            chat_id=reply_to_chat_id,
            photo=update.message.photo[-1].file_id
        )

    await update.message.reply_text("✅ Sent")


def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    # Reply button handler
    app.add_handler(
        CallbackQueryHandler(
            reply_button,
            pattern=r"^reply:"
        )
    )

    # Admin replies
    app.add_handler(
        MessageHandler(
            filters.Chat(chat_id=ADMIN_CHAT_ID)
            & (filters.TEXT | filters.PHOTO),
            send_admin_reply
        )
    )

    # User messages
    app.add_handler(
        MessageHandler(
            ~filters.Chat(chat_id=ADMIN_CHAT_ID)
            & (filters.TEXT | filters.PHOTO),
            handle_user_message
        )
    )

    print("Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
