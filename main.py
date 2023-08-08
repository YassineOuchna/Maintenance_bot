from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, ConversationHandler, MessageHandler, filters
from bot import logs

with open("./.gitignore/TOKEN.txt") as f:
    token = f.read().strip()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    hello_keyboard = ReplyKeyboardMarkup(
        [['/add', '/get', '/latest', '/edit']], resize_keyboard=True, one_time_keyboard=True)
    await update.message.reply_text("Hello! This is Viarezo's maintenance bot.", reply_markup=hello_keyboard)


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("I can help you manage all your maintenance needs through these commands : \n"
                                    "-> add : adding a maintenance \n"
                                    "-> past [number] : show the last [number] maintenances \n"
                                    "-> get : show a specific maintenance \n"
                                    "-> edit : modify a maintenance")

'''--- ADD CONVERSATION ---'''

ADD_NAME, ADD_PROCEDURE, ADD_DATE, ADD_LENGTH, ADD_MEMBERS, ADD_RISK, ADD_RCMT, ADD_CMT, ADD_TAGS = range(
    9)  # Different states, as intgers, of the "add" conversation


async def add(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Choose a name for your maintenance")
    # Global variable storing the maintenance throughout the conversation
    global maintenance
    maintenance = []
    return ADD_NAME


async def add_name(update, context: ContextTypes.DEFAULT_TYPE):
    name = update.message.text
    maintenance.append(name)
    await update.message.reply_text('Great! Now specify the procedure of the maintenance')
    return ADD_PROCEDURE


async def add_procedure(update, context: ContextTypes.DEFAULT_TYPE):
    procedure = update.message.text
    maintenance.append(procedure)
    await update.message.reply_text('Specify a date for the maintenance in the formate d-m-y')
    return ADD_DATE


async def add_date(update, context=ContextTypes.DEFAULT_TYPE):
    date = update.message.text
    maintenance.append(date)
    await update.message.reply_text('How many hours will it take ?')
    return ADD_LENGTH


async def add_length(update, context=ContextTypes.DEFAULT_TYPE):
    length = update.message.text
    if length.isdigit():
        maintenance.append(length)
        maintenance.append(update.message.from_user.username)
        await update.message.reply_text('Other than you, who else will help with this maintenance ? Don\'t forget to use - as a seperator')
        return ADD_MEMBERS
    else:
        await update.message.reply_text('Wrong input, I need an integer')
        return ADD_LENGTH


async def add_members(update, context=ContextTypes.DEFAULT_TYPE):
    members = update.message.text
    # adding the username as the default owner of the maintenance
    maintenance.append(members)
    await update.message.reply_text('Rate the risk of the maintenance from 0 to 5')
    return ADD_RISK


async def add_risk(update, context=ContextTypes.DEFAULT_TYPE):
    risk = update.message.text
    if risk.isdigit():
        maintenance.append(risk)
        await update.message.reply_text('Great! Now you can add secondary stuff like comments and tags or /skip if you don\'t want to.')
        await update.message.reply_text('Add a risk comment')
        return ADD_RCMT
    else:
        await update.message.reply_text('Wrong input, I need an integer')
        return ADD_RISK


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
                                    f':file_folder: id = {maintenance_id} \n'
                                    f':duck: Nom = {maintenance[0]} \n'
                                    f':newspaper: Déroulé = {maintenance[1]} \n'
                                    f':alarm_clock: Date={maintenance[2]} \n'
                                    f':hourglass_flowing_sand: Durée ={maintenance[3]} \n'
                                    f':bust_in_silhouette: Propriétaire = {maintenance[4]} \n'
                                    f':busts_in_silhouette: Membres = {maintenance[5]} \n'
                                    '...')
    return ConversationHandler.END


async def skip(update, context=ContextTypes.DEFAULT_TYPE):
    maintenance_id = logs.add(maintenance[0], maintenance[1], maintenance[2],
                              maintenance[3], maintenance[4], maintenance[5], maintenance[6])
    await update.message.reply_text(f'You have now added the following maintenance : \n'
                                    f':file_folder: id = {maintenance_id} \n'
                                    f':duck: Nom = {maintenance[0]} \n'
                                    f':newspaper: Déroulé = {maintenance[1]} \n'
                                    f':alarm_clock: Date={maintenance[2]} \n'
                                    f':hourglass_flowing_sand: Durée ={maintenance[3]} \n'
                                    f':bust_in_silhouette: Propriétaire = {maintenance[4]} \n'
                                    f':busts_in_silhouette: Membres = {maintenance[5]} \n'
                                    '...')
    return ConversationHandler.END

'''--- GET CONVERSATION ---'''

GET_NAME = range(1)


async def get(update, context=ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('What\'s the name of the maintenance ?')
    return GET_NAME


async def querry(update, context=ContextTypes.DEFAULT_TYPE):
    name_given = update.message.text
    querry_result = logs.retrieve(name_given)
    if querry_result == None:
        await update.message.reply.text('Oops! There is no such maintenance.')
    else:
        await update.message.reply.text('Found the following maintenance : \n'
                                        f':file_folder: id = {querry_result[0]} \n'
                                        f':duck: Nom = {querry_result[1]} \n'
                                        f':newspaper: Déroulé = {querry_result[2]} \n'
                                        f':alarm_clock: Date={querry_result[3]} \n'
                                        f':hourglass_flowing_sand: Durée ={querry_result[4]} \n'
                                        f':bust_in_silhouette: Propriétaire = {querry_result[5]} \n'
                                        f':busts_in_silhouette: Membres = {querry_result[6]} \n'
                                        f':warning: Risk : {querry_result[7]}\n'
                                        f'-{querry_result[8]}'
                                        '...')
    return ConversationHandler.END

'''--- LATEST CONVERSATION ---'''


async def cancel(update, context=ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Current procedure has been canceled, send /help for more information.')
    return ConversationHandler.END

app = ApplicationBuilder().token(token).build()

app.add_handler(CommandHandler("start", start))

app.add_handler(CommandHandler("help", help))

conv_handler_add = ConversationHandler(
    entry_points=[CommandHandler('add', add)],
    states={
        ADD_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_name)],
        ADD_PROCEDURE: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_procedure)],
        ADD_DATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_date)],
        ADD_LENGTH: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_length)],
        ADD_MEMBERS: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_members)],
        ADD_RISK: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_risk), CommandHandler('skip', skip)],
        ADD_RCMT: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_rcmt), CommandHandler('skip', skip)],
        ADD_CMT: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_cmt), CommandHandler('skip', skip)],
        ADD_TAGS: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_tags),
                   CommandHandler('skip', skip)]
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)

conv_handler_get = ConversationHandler(
    entry_points=[CommandHandler('get', get)],
    states={GET_NAME: [MessageHandler(
        filters.TEXT & ~filters.COMMAND, querry)]},
    fallbacks=[CommandHandler('cancel', cancel)]
)
app.add_handler(conv_handler_add)
app.add_handler(conv_handler_get)
app.run_polling()
