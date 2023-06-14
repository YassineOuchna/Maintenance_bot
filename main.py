from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, ConversationHandler, MessageHandler, filters
from bot import logs

with open("./.gitignore/TOKEN.txt") as f:
    token = f.read().strip()

ADD_NAME, ADD_TYPE, ADD_DATE, ADD_LENGHT, ADD_MEMBERS, ADD_RISK, ADD_RCMT, ADD_CMT, ADD_TAGS = range(
    9)


async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Hello! This is Viarezo's maintenance bot.")


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("I can help you manage all your maintenance needs through these commands : \n"
                                    "-> add : adding a maintenance \n"
                                    "-> past [int] : show the last [int] maintenances \n"
                                    "-> get : show a specific maintenance \n"
                                    "-> edit : modify a maintenance")


async def add(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Choose a name for your maintenance")
    global maintenance
    maintenance = []
    return ADD_NAME


async def add_name(update, context: ContextTypes.DEFAULT_TYPE):
    name = update.message.text
    maintenance.append(name)
    await update.message.reply_text('Great! Now specify the type of the maintenance')
    return ADD_TYPE


async def add_type(update, context: ContextTypes.DEFAULT_TYPE):
    type = update.message.text
    maintenance.append(type)
    await update.message.reply_text('Specify a date for the maintenance in the formate d-m-y')
    return ADD_DATE


async def add_date(update, context=ContextTypes.DEFAULT_TYPE):
    date = update.message.text
    maintenance.append(date)
    await update.message.reply_text('How many hours will it take ?')
    return ADD_LENGHT


async def add_lenght(update, context=ContextTypes.DEFAULT_TYPE):
    lenght = update.message.text
    maintenance.append(lenght)
    maintenance.append(update.message.from_user.username)
    await update.message.reply_text('Other than you, who else will help with this maintenance ? Don\'t forget to use - as a seperator')
    return ADD_MEMBERS


async def add_members(update, context=ContextTypes.DEFAULT_TYPE):
    members = update.message.text
    # adding the username as the default owner of the maintenance
    maintenance.append(members)
    await update.message.reply_text('Rate the risk of the maintenance from 0 to 5')
    return ADD_RISK


async def add_risk(update, context=ContextTypes.DEFAULT_TYPE):
    risk = update.message.text
    maintenance.append(risk)
    await update.message.reply_text('Great! Now you can add a risk comment or /skip if you don\'t want to')
    logs.add(maintenance[0], maintenance[1], maintenance[2],
             maintenance[3], maintenance[4], maintenance[5], maintenance[6])
    return ConversationHandler.END

app = ApplicationBuilder().token(token).build()

app.add_handler(CommandHandler("hello", hello))

app.add_handler(CommandHandler("help", help))

conv_handler = ConversationHandler(
    entry_points=[CommandHandler('add', add)],
    fallbacks=[],

    states={
        ADD_NAME: [MessageHandler(filters.TEXT, add_name)],
        ADD_TYPE: [MessageHandler(filters.TEXT, add_type)],
        ADD_DATE: [MessageHandler(filters.TEXT, add_date)],
        ADD_LENGHT: [MessageHandler(filters.TEXT, add_lenght)],
        ADD_MEMBERS: [MessageHandler(filters.TEXT, add_members)],
        ADD_RISK: [MessageHandler(filters.TEXT, add_risk)],
    },
)
app.add_handler(conv_handler)
app.run_polling()
