from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes


async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f"Hello! This is Viarezo's maintenance bot.")


app = ApplicationBuilder().token(
    "5909711949:AAHM_tD7Q4rGpxIHNKAeQVUrle_PYI_sdFM").build()

app.add_handler(CommandHandler("hello", hello))

app.run_polling()
