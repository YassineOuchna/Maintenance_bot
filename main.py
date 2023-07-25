from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, ConversationHandler, MessageHandler, filters
from bot import logs

with open("./.gitignore/TOKEN.txt") as f:
    token = f.read().strip()

ADD_NAME, ADD_TYPE, ADD_DATE, ADD_LENGTH, ADD_MEMBERS, ADD_RISK, ADD_RCMT, ADD_CMT, ADD_TAGS = range(
    9)  # Different states, as intgers, of the "add" conversation


async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Hello! This is Viarezo's maintenance bot.")


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("I can help you manage all your maintenance needs through these commands : \n"
                                    "-> add : adding a maintenance \n"
                                    "-> past [number] : show the last [number] maintenances \n"
                                    "-> get : show a specific maintenance \n"
                                    "-> edit : modify a maintenance")


async def add(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Choose a name for your maintenance")
    # Global variable storing the maintenance throughout the conversation
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
    return ADD_LENGTH


async def add_length(update, context=ContextTypes.DEFAULT_TYPE):
    length = update.message.text
    maintenance.append(length)
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
    await update.message.reply_text('Great! Now you can add secondary stuff like comments and tags or /skip if you don\'t want to.')
    await update.message.reply_text('Add a risk comment')
    return ADD_RCMT


async def add_rcmt(update, context=ContextTypes.DEFAULT_TYPE):
    risk_cmnt = update.message.text
    maintenance.append(risk_cmnt)
    await update.message.reply_text('You can also add a general comment')
    return ADD_CMT


async def add_cmt(update, context=ContextTypes.DEFAULT_TYPE):
    cmnt = update.message.text
    maintenance.append(cmnt)
    await update.message.reply_text('You can also add tags')
    return ADD_TAGS


async def add_tags(update, context=ContextTypes.DEFAULT_TYPE):
    tags = update.message.text
    maintenance.append(tags)
    maintenance_id = logs.add(maintenance[0], maintenance[1], maintenance[2],
                              maintenance[3], maintenance[4], maintenance[5], maintenance[6],
                              maintenance[7], maintenance[8], maintenance[9])
    await update.message.reply_text(f'You have now added the following maintenance : \n'
                                    f'id = {maintenance_id} \n'
                                    f'name = {maintenance[0]} \n'
                                    f'type = {maintenance[1]} \n'
                                    f'date={maintenance[2]} \n'
                                    f'length ={maintenance[3]} \n'
                                    f'owner = {maintenance[4]} \n'
                                    f'members = {maintenance[5]} \n'
                                    '...')
    return ConversationHandler.END


async def skip(update, context=ContextTypes.DEFAULT_TYPE):
    maintenance_id = logs.add(maintenance[0], maintenance[1], maintenance[2],
                              maintenance[3], maintenance[4], maintenance[5], maintenance[6])
    await update.message.reply_text(f'You have now added the following maintenance : \n'
                                    f'id = {maintenance_id} \n'
                                    f'name = {maintenance[0]} \n'
                                    f'type = {maintenance[1]} \n'
                                    f'date={maintenance[2]} \n'
                                    f'length ={maintenance[3]}\n'
                                    f'owner = {maintenance[4]} \n'
                                    f'members = {maintenance[5]}\n'
                                    '...')
    return ConversationHandler.END


async def cancel(update, context=ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Current procedure has been canceled, send /help for more information.')
    return ConversationHandler.END

app = ApplicationBuilder().token(token).build()

app.add_handler(CommandHandler("hello", hello))

app.add_handler(CommandHandler("help", help))

conv_handler = ConversationHandler(
    entry_points=[CommandHandler('add', add)],
    fallbacks=[CommandHandler("cancel", cancel)],

    states={
        ADD_NAME: [MessageHandler(filters.TEXT, add_name)],
        ADD_TYPE: [MessageHandler(filters.TEXT, add_type)],
        ADD_DATE: [MessageHandler(filters.TEXT, add_date)],
        ADD_LENGTH: [MessageHandler(filters.TEXT, add_length)],
        ADD_MEMBERS: [MessageHandler(filters.TEXT, add_members)],
        ADD_RISK: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_risk), CommandHandler('skip', skip)],
        ADD_RCMT: [MessageHandler(filters.TEXT, add_rcmt), CommandHandler('skip', skip)],
        ADD_CMT: [MessageHandler(filters.TEXT, add_cmt), CommandHandler('skip', skip)],
        ADD_TAGS: [MessageHandler(filters.TEXT, add_tags),
                   CommandHandler('skip', skip)]
    },
)
app.add_handler(conv_handler)
app.run_polling()
