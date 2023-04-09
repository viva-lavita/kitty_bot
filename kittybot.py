import requests
import os

from dotenv import load_dotenv
from telegram import Bot, ReplyKeyboardMarkup
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater


load_dotenv()

token = os.getenv('TOKEN')
chat_sid = os.getenv('CHAT_ID')
bot = Bot(token=token)
updater = Updater(token=token)
URL = 'https://api.thecatapi.com/v1/images/search'
text = 'Вам телеграмма!'  # мб потом сюда дописать словарь?


def get_new_image():
    response = requests.get(URL).json()
    random_cat = response[0].get('url')
    return random_cat


def new_cat(update, context):
    chat = update.effective_chat
    context.bot.send_photo(chat.id, get_new_image())


def say_hi(update, context):
    chat = update.effective_chat
    context.bot.send_message(chat_id=chat.id, text='Привет, я KittyBot!')


def wake_up(update, context):
    chat = update.effective_chat
    name = update.message.chat.first_name
    button = ReplyKeyboardMarkup([['/newcat']], resize_keyboard=True)

    context.bot.send_message(
        chat_id=chat.id,
        text='Привет, {}. Посмотри, какого котика я тебе нашёл'.format(name),
        reply_markup=button,
        )

    context.bot.send_photo(chat.id, get_new_image())


def send_message(message):
    # Обрати внимение, это тест отправки из кода, в собственный (chat_sid) чат
    Bot.send_message(chat_sid, message)


updater.dispatcher.add_handler(CommandHandler('start', wake_up))

updater.dispatcher.add_handler(CommandHandler('newcat', new_cat))

updater.dispatcher.add_handler(MessageHandler(Filters.text, say_hi))

updater.start_polling(poll_interval=10.0)  # переодичность, в секундах флоат

updater.idle()
