import logging

import update as update
from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
import dotenv
from dotenv import load_dotenv
import os

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("Help!")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    from openai import OpenAI
    gpt_token = os.environ['GPT_TOKEN']
    client = OpenAI(
        # defaults to os.environ.get("OPENAI_API_KEY")
        api_key=gpt_token,
    )
    if update.message.reply_to_message and len(ANSWERS) != 0:
        messages = [
            {"role": "assistant", "content": ANSWERS[-1]},
            {"role": "user", "content": update.message.text, }
        ]
    else:
        messages = [
            {"role": "user", "content": update.message.text, }
            ]
    chat_completion = client.chat.completions.create(
        messages=messages,
        model="gpt-3.5-turbo",
    )

    # put in array the answer
    ANSWERS.append(chat_completion.choices[0].message.content)
    await update.message.reply_text(ANSWERS[-1])


def main() -> None:
    """Start the bot."""
    load_dotenv()
    ptb_token = os.environ['PTB_TOKEN']
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(ptb_token).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    ANSWERS = []
    main()


