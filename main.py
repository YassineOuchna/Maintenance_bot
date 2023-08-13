from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, ConversationHandler, MessageHandler, filters
from bot import logs
from bot import cur, conn

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
                                    u'\U0001F4C2' f' id : {maintenance_id} \n'
                                    '\n'
                                    u'\U0001F986' f' Nom = {maintenance[0]} \n'
                                    '\n'
                                    u'\U0001F4F0' f' Déroulé : {maintenance[1]} \n'
                                    '\n'
                                    u'\U000023F0' f' Date : {maintenance[2]} \n'
                                    '\n'
                                    u'\U000023F3' f' Durée : {maintenance[3]} \n'
                                    '\n'
                                    u'\U0001F464' f': Propriétaire : {maintenance[4]} \n'
                                    f':busts_in_silhouette: Membres = {maintenance[5]} \n'
                                    '...')
    return ConversationHandler.END


async def skip(update, context=ContextTypes.DEFAULT_TYPE):
    maintenance_id = logs.add(maintenance[0], maintenance[1], maintenance[2],
                              maintenance[3], maintenance[4], maintenance[5], maintenance[6])
    await update.message.reply_text(f'You have now added the following maintenance : \n'
                                    u'\U0001F4C2' f' id : {maintenance_id} \n'
                                    '\n'
                                    u'\U0001F986' f' Nom = {maintenance[0]} \n'
                                    '\n'
                                    u'\U0001F4F0' f' Déroulé : {maintenance[1]} \n'
                                    '\n'
                                    u'\U000023F0' f' Date : {maintenance[2]} \n'
                                    '\n'
                                    u'\U000023F3' f' Durée : {maintenance[3]} \n'
                                    '\n'
                                    u'\U0001F464' f': Propriétaire : {maintenance[4]} \n'
                                    u'\U0001F465' f' Membres : {maintenance[5]} \n'
                                    '...')
    return ConversationHandler.END

'''--- GET CONVERSATION ---'''

GET_NAME = range(1)


async def get(update, context=ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('What\'s the name of the maintenance ?')
    return GET_NAME


async def querry(update, context=ContextTypes.DEFAULT_TYPE):
    name_given = update.message.text
    query_result = logs.retrieve_by_name(name_given)
    if query_result == None:
        await update.message.reply_text('Oops! There is no such maintenance.')
    else:
        await update.message.reply_text('Found the following maintenance : \n'
                                        u'\U0001F4C2' f' id : {query_result[0]} \n'
                                        '\n'
                                        u'\U0001F986' f' Nom : {query_result[1]} \n'
                                        '\n'
                                        u'\U0001F4F0' f' Déroulé : {query_result[2]} \n'
                                        '\n'
                                        u'\U000023F0' f' Date : {query_result[3]} \n'
                                        '\n'
                                        u'\U000023F3' f' Durée : {query_result[4]} \n'
                                        '\n'
                                        u'\U0001F464' f' Propriétaire : {query_result[5]} \n'
                                        '\n'
                                        u'\U0001F465' f' Membres : {query_result[6]} \n'
                                        '\n'
                                        u'\U000026A0' f' Risk : {query_result[7]}\n'
                                        f'-{query_result[8]} \n'
                                        '...')
    return ConversationHandler.END

'''--- LATEST ---'''


async def latest(update, context=ContextTypes.DEFAULT_TYPE):
    latest_three = logs.latest(3)
    for query_result in latest_three:
        await update.message.reply_text(u'\U0001F4C2' f' id : {query_result[0]} \n'
                                        '\n'
                                        u'\U0001F986' f' Nom : {query_result[1]} \n'
                                        '\n'
                                        u'\U0001F4F0' f' Déroulé : {query_result[2]} \n'
                                        '\n'
                                        u'\U000023F0' f' Date : {query_result[3]} \n'
                                        '\n'
                                        u'\U000023F3' f' Durée : {query_result[4]} \n'
                                        '\n'
                                        u'\U0001F464' f' Propriétaire : {query_result[5]} \n'
                                        '\n'
                                        u'\U0001F465' f' Membres : {query_result[6]} \n'
                                        '\n'
                                        u'\U000026A0' f' Risk : {query_result[7]}\n'
                                        f'-{query_result[8]} \n'
                                        '\n'
                                        u'\U0000270D' f' Commentaires : {query_result[9]} \n'
                                        '\n'
                                        u'\U0001F4CC' f' Tags : {query_result[10]}')


'''--- EDIT CONVERSATION ---'''

EDIT_FIND, EDIT_WHAT = range(2)


async def edit_find(update, context=ContextTypes.DEFAULT_TYPE):
    biggest_id = cur.execute("SELECT max(id) from maintenances").fetchone()[0]
    await update.message.reply_text("what is the id of the maintenance that you want to edit ? \n"
                                    '\n'
                                    f'The current most recent maintenance has an id of {biggest_id}')
    return EDIT_FIND


async def edit_what(update, context=ContextTypes.DEFAULT_TYPE):
    editing_id = update.message.text
    query_result = logs.retrieve_by_id(editing_id)
    if query_result == None:
        await update.message.reply_text('No such maintenance exists')
        return EDIT_FIND
    else:
        await update.message.reply_text(u'\U0001F4C2' f' id : {query_result[0]} \n'
                                        '\n'
                                        u'\U0001F986' f' name : {query_result[1]} \n'
                                        '\n'
                                        u'\U0001F4F0' f' procedure : {query_result[2]} \n'
                                        '\n'
                                        u'\U000023F0' f' date : {query_result[3]} \n'
                                        '\n'
                                        u'\U000023F3' f' length : {query_result[4]} \n'
                                        '\n'
                                        u'\U0001F464' f' owner : {query_result[5]} \n'
                                        '\n'
                                        u'\U0001F465' f' members : {query_result[6]} \n'
                                        '\n'
                                        u'\U000026A0' f' risk_lvl : {query_result[7]}\n'
                                        f'risk_cmt -{query_result[8]} \n'
                                        '\n'
                                        u'\U0000270D' f' comment : {query_result[9]} \n'
                                        '\n'
                                        u'\U0001F4CC' f' tags : {query_result[10]}')
        await update.message.reply_text('')
        return EDIT_WHAT


async def cancel(update, context=ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Current procedure has been canceled, send /help for more information.')
    return ConversationHandler.END

app = ApplicationBuilder().token(token).build()

app.add_handler(CommandHandler("start", start))

app.add_handler(CommandHandler("help", help))

app.add_handler(CommandHandler('latest', latest))

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
