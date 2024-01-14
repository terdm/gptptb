from asyncio import Queue

from telegram.ext import Updater, CommandHandler, MessageHandler, filters, Application, ContextTypes
from telegram import Update, ForceReply
import os
from dotenv import load_dotenv
# def start(update, context):
#     update.message.reply_text('Hello, welcome to your bot!')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )

async def message_handler(update :Update, context):
    #print('message_handler')
    if update.message.reply_to_message:
        # Get the ID of the message that this message is replying to
        replied_message_id = update.message.reply_to_message.message_id

        # Get the whole message chain using the replied message ID
        message_chain = [update.message]
        print(message_chain)
        current_message = update.message.reply_to_message
        while current_message.reply_to_message:
            message_chain.insert(0, current_message.reply_to_message)
            current_message = current_message.reply_to_message

        # Print the message chain
        for message in message_chain:
            print(f"{message.from_user.username}: {message.text}")
            ANSWERS.append(message.text)
    ANSWERS.append('dummy')
    print(ANSWERS)
    print(ANSWERS[-1])

    await update.message.reply_text(ANSWERS[-1])
def main():
    load_dotenv()
    ptb_token = os.environ['PTB_TOKEN']
    application = Application.builder().token(ptb_token).build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT, message_handler))

    application.run_polling(allowed_updates=Update.ALL_TYPES)
    #updater.idle()

if __name__ == '__main__':
    ANSWERS = []
    main()
