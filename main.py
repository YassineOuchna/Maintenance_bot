from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, ConversationHandler, MessageHandler, filters
from bot import logs

with open("./.gitignore/TOKEN.txt") as f:
    token = f.read().strip()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    hello_keyboard = ReplyKeyboardMarkup(
        [['/add', '/get', '/latest', '/edit']], resize_keyboard=True, one_time_keyboard=True)
    await update.message.reply_text("Hello! This is Viarézo's maintenance bot. \n"
                                    '\n'
                                    "You can send /help for a description of different commands.", reply_markup=hello_keyboard)


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Vous pouvez utiliser les commandes suivantes pour gérer vos maintenances : \n"
                                    '\n'
                                    "-> /add : Ajouter une maintenance \n"
                                    '\n'
                                    "-> /latest : Visualiser les 3 dernières maintenances \n"
                                    '\n'
                                    "-> /get :  Visualiser une maintenance dont vous connaissez son nom \n"
                                    '\n'
                                    "-> /edit : modifier une maintenance dont vous connaissez son id \n"
                                    '\n'
                                    "-> /cancel : Annuler la conversation/procédure au courant. \n"
                                    '\n'
                                    '-> /delete : Supprimer une maintenance.')

'''--- ADD CONVERSATION ---'''

ADD_NAME, ADD_PROCEDURE, ADD_DATE, ADD_LENGTH, ADD_MEMBERS, ADD_RISK, ADD_RCMT, ADD_CMT, ADD_TAGS = range(
    9)  # Different states, as intgers, of the "add" conversation


async def add(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Choose a name for your maintenance")
    # Global variable storing the maintenance throughout the conversation
    global maintenance
    maintenance = []
    return ADD_NAME   # returns the next state/step of the conversation


async def add_name(update, context: ContextTypes.DEFAULT_TYPE):
    name = update.message.text
    maintenance.append(name)
    await update.message.reply_text('Great! Now specify the procedure of the maintenance')
    return ADD_PROCEDURE


async def add_procedure(update, context: ContextTypes.DEFAULT_TYPE):
    procedure = update.message.text
    maintenance.append(procedure)
    await update.message.reply_text('Specify a date for the maintenance in the formate dd/mm/yy')
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
    if risk.isdigit() and int(risk) in range(0, 6):
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
                                    u'\U0001F465' f' Membres = {maintenance[5]} \n'
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
                                    u'\U0001F464' f' Propriétaire : {maintenance[4]} \n'
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
        await update.message.reply_text('Oops! There is no such maintenance. You can see the name of the /latest three maintenances.')
    else:
        await update.message.reply_text('Found the following maintenance : \n'
                                        '\n'
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
    latest_three = logs.latest()
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

EDIT_FIND, EDIT_SOMETHING, EDIT_TO, FINISHED_EDITING = range(4)


async def edit(update, context=ContextTypes.DEFAULT_TYPE):
    biggest_id = logs.latest_id()
    await update.message.reply_text("What is the id of the maintenance that you want to edit ? \n"
                                    '\n'
                                    f'The current most recent maintenance has an id of {biggest_id}')
    return EDIT_FIND


async def edit_find(update, context=ContextTypes.DEFAULT_TYPE):
    global editing_id
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
                                        f'risk_cmt : {query_result[8]} \n'
                                        '\n'
                                        u'\U0000270D' f' comment : {query_result[9]} \n'
                                        '\n'
                                        u'\U0001F4CC' f' tags : {query_result[10]}')
        edit_keyboard = ReplyKeyboardMarkup(
            [['name', 'date', 'length', 'members', 'risk_lvl']], resize_keyboard=True, one_time_keyboard=True)
        await update.message.reply_text('What would you like to edit ?', reply_markup=edit_keyboard)
        return EDIT_SOMETHING


async def edit_something(update: Update, context=ContextTypes.DEFAULT_TYPE):
    global column
    column = update.message.text
    if column in ['name', 'date', 'length', 'members', 'risk_lvl', 'owner', 'procedure', 'comment', 'tags']:
        await update.message.reply_text('What would you like to change it to ? \n'
                                        '\n'
                                        'Reminder to follow the data types of these columns : \n'
                                        '\n'
                                        'date : dd/mm/yy \n'
                                        'length : interger (hrs) \n'
                                        'members : members seperated by - \n'
                                        'risk_lvl : integer 0-5 \n'
                                        )
        return EDIT_TO
    else:
        await update.message.reply_text('No such column exists / wrong syntaxe.')
        return EDIT_SOMETHING


async def edit_to(update, context=ContextTypes.DEFAULT_TYPE):
    new_value = update.message.text
    edits = (column, new_value)
    logs.edit(editing_id, edits)
    await update.message.reply_text('What other column do you want to edit ? \n'
                                    'If finished, send /finished_editing')
    return EDIT_SOMETHING


async def finished_editing(update, context=ContextTypes.DEFAULT_TYPE):
    query_result = logs.retrieve_by_id(editing_id)
    await update.message.reply_text('Here is the new edited maintenance :'
                                    '\n'
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
                                    '\n'
                                    u'\U0000270D' f' Commentaires : {query_result[9]} \n'
                                    '\n'
                                    u'\U0001F4CC' f' Tags : {query_result[10]}')
    return ConversationHandler.END


'''--- DELETE CONVERSATION ---'''

AREYOUSURE, DELETE = range(2)


async def delete(update, context=ContextTypes.DEFAULT_TYPE):
    biggest_id = logs.latest_id()
    await update.message.reply_text("What is the id of the maintenance that you want to PERMANENTLY delete ? \n"
                                    '\n'
                                    f'The current most recent maintenance has an id of {biggest_id}')
    return AREYOUSURE


async def are_you_sure(update, context=ContextTypes.DEFAULT_TYPE):
    global id_to_delete
    id_to_delete = update.message.text
    query_result = logs.retrieve_by_id(id_to_delete)
    if query_result == None:
        await update.message.reply_text('No such maintenance exists')
        return AREYOUSURE
    else:
        yes_no_keyboard = ReplyKeyboardMarkup(
            [['yes', 'no']], resize_keyboard=True, one_time_keyboard=True)
        await update.message.reply_text('Are you sure this is the maintenance that you want to delete (yes/no) ? :'
                                        '\n'
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
                                        '\n'
                                        u'\U0000270D' f' Commentaires : {query_result[9]} \n'
                                        '\n'
                                        u'\U0001F4CC' f' Tags : {query_result[10]}', reply_markup=yes_no_keyboard)

    return DELETE


async def sure(update, context=ContextTypes.DEFAULT_TYPE):
    response = update.message.text
    if response == 'yes':
        logs.delete(id_to_delete)
        await update.message.reply('Maintenance have been deleted')
        return ConversationHandler.END
    else:
        await update.message.reply_text('If you don\'t know the id you can see the /latest three maintenances.')
        return AREYOUSURE


async def cancel(update, context=ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Current conversation ended, send /help for more information.')
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

conv_handler_edit = ConversationHandler(
    entry_points=[CommandHandler('edit', edit)],
    states={EDIT_FIND: [MessageHandler(filters.TEXT & ~filters.COMMAND, edit_find)],
            EDIT_SOMETHING: [MessageHandler(filters.TEXT & ~filters.COMMAND, edit_something), CommandHandler(
                'finished_editing', finished_editing)],
            EDIT_TO: [MessageHandler(filters.TEXT & ~filters.COMMAND, edit_to), CommandHandler(
                'finished_editing', finished_editing)]
            },
    fallbacks=[CommandHandler('cancel', cancel)]
)

conv_handler_delete = ConversationHandler(
    entry_points=[CommandHandler('delete', delete)],
    states={AREYOUSURE: [MessageHandler(
        filters.TEXT & ~filters.COMMAND, are_you_sure)],
        DELETE: [MessageHandler(filters.TEXT & ~filters.COMMAND, sure)]},
    fallbacks=[CommandHandler('cancel', cancel)]
)

app.add_handler(conv_handler_delete)
app.add_handler(conv_handler_edit)
app.add_handler(conv_handler_add)
app.add_handler(conv_handler_get)
app.run_polling()
