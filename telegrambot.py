import django
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'core.settings'
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
django.setup()

import logging
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler, ApplicationBuilder
from telegram.ext import *

from profiles.models import userProfile

API_KEY = '5644982761:AAEVn3itxbBw2a3N9kjjDr29mxkpW34RaU4'



print('Bot Started')


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Silahkan registarsi telegram anda")
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Ketik /update username no_hp")
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Contoh : /update AA0200001 08111111111")
    
async def update_id(update: Update, context: ContextTypes):
    data = userProfile.objects.select_related('user').all()
    npp = update.message.text.split(' ')
    if (len(npp) != 3):
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Format Anda Salah")
    elif not data.filter(no_hp=npp[2]).exists():
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Silahkan update No HP Anda. Klik : http://localhost:8000/login/")
    else:
        data = userProfile.objects.select_related('user').filter(user__username=npp[1])
        if(data.exists()):
            userProfile.objects.select_related('user').filter(user__username=npp[1]).update(id_telegram=update.effective_chat.id)
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Terima Kasih")

# def handle_message(update, context):
#     text = str(update.message.text).lower()
#     update.message.z("Hi from telegram bot")
#     print(text)

if __name__ == '__main__':

    application = ApplicationBuilder().token(API_KEY).build()
    # updater = Updater(API_KEY, use_context=True)
    # dp = updater.dispatcher

    start_handler = CommandHandler('start',start)
    update_handler = CommandHandler('update', update_id)

    application.add_handler(start_handler)
    application.add_handler(update_handler)

    # application.start_polling(1.0)
    application.run_polling()
    application.idle()