from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, ConversationHandler, MessageHandler
from bot import logs


async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Hello! This is Viarezo's maintenance bot.")


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("I can help you manage all your maintenance needs through these commands : \n **adding a maintenance** ")


async def add(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Choose a name for your maintenance")
    return 0


def add_name(update, context):
    name = update.message.text
    update.message.reply_text(f'great! you chose {name}')
    return ConversationHandler.END


app = ApplicationBuilder().token(
    "5909711949:AAHM_tD7Q4rGpxIHNKAeQVUrle_PYI_sdFM").build()

app.add_handler(CommandHandler("hello", hello))

app.add_handler(CommandHandler("help", help))

conv_handler = ConversationHandler(
    entry_points=[CommandHandler('add', add)],
    fallbacks=[],

    states={
        0: [CommandHandler('name', add_name)],
    },
)
app.add_handler(conv_handler)
app.run_polling()
