from telegram import Bot, ReplyKeyboardMarkup
from telegram.ext import Updater, Filters, MessageHandler, CommandHandler
import requests
import datetime
import os
from dotenv import load_dotenv
import random
from random import randint



load_dotenv()
secret_token =  os.getenv("TOKEN")
chat_id = os.getenv('CHAT_ID')


URL = 'https://api.thecatapi.com/v1/images/search'
URL1 = "https://api.thedogapi.com/v1/images/search"





updater = Updater(token=secret_token)
bot = Bot(token=secret_token)


def say_hi(update, context):
    chat = update.effective_chat
    context.bot.send_message(chat_id=chat.id,
                             text=f'Привет, {chat.first_name}, я raw raw raw')
def give_time(update, context):
    now = datetime.datetime.now()
    chat = update.effective_chat

    context.bot.send_message(chat_id=chat.id,
                             text=now.strftime('%H:%M:%S'))

def give_date(update, context):
    now = datetime.datetime.now()
    chat = update.effective_chat

    context.bot.send_message(chat_id=chat.id,
                             text=now.strftime('%d.%m.%Y'))


def get_new_image(URL, URL1):
    try:
        response = requests.get(URL).json()
    except Exception as e:
        print(e)
        new_url = URL1
        response = requests.get(new_url).json()

    return response[0]['url']



def get_new_image2():
    x = randint(1, 121)
    url2 = 'https://randomfox.ca/images/' + str(x) + '.jpg'
    response = requests.get(url2).json()
    print(response)
    return response[0]['url']




def wake_up(update, context):
    chat = update.effective_chat
    name = chat.first_name
    buttons = ReplyKeyboardMarkup([
        ['/newcat', '/start', "/date"],
        ["/newdog", "/meme", "/time"],

    ], resize_keyboard=True)
    context.bot.send_message(chat_id=chat.id,
                             text=
                             f"""Спасибо, что включили меня, {name}, чем могу быть полезен?:) Еды пока нет, могу предложить котиков, для этого нажмите на кнопку /newcat, чтобы узнать который час нажмите на кнопку  /time""",
                             reply_markup=buttons
    )
    bot.send_photo(chat.id, get_new_image(URL, URL1))


def give_new_cat(update, context):
    chat = update.effective_chat
    context.bot.send_photo(chat.id, get_new_image(URL, URL1))

def give_new_dog(update, context):
    chat = update.effective_chat
    context.bot.send_photo(chat.id, get_new_image(URL1, URL))

def give_new_meme(update, context):
    chat = update.effective_chat
    context.bot.send_photo(chat.id, get_new_image2())


def main():
    updater.dispatcher.add_handler(CommandHandler('start', wake_up))
    updater.dispatcher.add_handler(CommandHandler('newcat', give_new_cat))
    updater.dispatcher.add_handler(CommandHandler('newdog', give_new_dog))
    updater.dispatcher.add_handler(CommandHandler("meme", give_new_meme))
    updater.dispatcher.add_handler(CommandHandler('time', give_time))
    updater.dispatcher.add_handler(CommandHandler('date', give_date))
    updater.dispatcher.add_handler(MessageHandler(Filters.text, say_hi))
    updater.start_polling()


if __name__ == '__main__':
    main()