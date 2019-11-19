import os
import telepot
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
import argparse
from flask import Flask, request
from telepot.loop import OrderedWebhook
from pokemonTrainer import *
import re

def renderRespuestaTipo(my_keyboard, lines):
    if len(lines) <1:
        return
    buttons = []
    for line in lines:
        buttons.append(InlineKeyboardButton(text=str(line.split(" ")[3]), callback_data=line))
    
    my_keyboard.append(buttons)
    
    return my_keyboard
    
def sendData(chat_id, bot, response):
    if bot == None:
        return
    
    listBotonEfectividad = []
    my_keyboard = []
    textToSend = ""
    
    for line in response.split("\n"):
        if "<botonefectividad>" in line:
            listBotonEfectividad.append(line.split(">")[1])
            #my_keyboard = renderRespuestaTipo(my_keyboard, line.split(">")[1])
        else:
            textToSend += line + "\n"
    
    if len(listBotonEfectividad) > 0:
        my_keyboard =  renderRespuestaTipo(my_keyboard, listBotonEfectividad)
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=my_keyboard)
    bot.sendMessage(chat_id, textToSend, reply_markup=keyboard)

def on_callback_query(msg):
    query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
    response = processCommand(query_data)
    sendData(from_id, bot, response)

def on_chat_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    if content_type == 'text':
        response = processCommand(msg["text"])
    else:
        response = "error"

    sendData(chat_id, bot, response)

def on_inline_query(msg):
    pass

def on_chosen_inline_result(msg):
    pass

def processCommand(text):
    command = text.split(" ")[0].lower()
    if command == "/start":
        return hacerPregunta()        
    if "/evaluar" in command:
        return procesarRespuesta(text.replace("/evaluar ", ""))    
    if "/tipos" in command:
        return getTypes()
    if "/efectividades" in command:
        return "trabajando en ello"
    else:
        return "Comando desconocido"

# Main starts here
token = str(os.environ["telegram_token"])
bot = telepot.Bot(token) # Bot is created from the telepot class
app = Flask(__name__)
URL = str(os.environ["telegram_url"])
webhook = OrderedWebhook(bot, {'chat': on_chat_message,
                               'callback_query': on_callback_query,
                               'inline_query': on_inline_query,
                               'chosen_inline_result': on_chosen_inline_result})

@app.route('/', methods=['GET', 'POST'])
def pass_update():
    webhook.feed(request.data)
    return 'OK'

if __name__ == '__main__':
    app.run()
    printf("Executed the run")
    
if __name__ != '__main__':
    try:
        bot.setWebhook(URL)
    # Sometimes it would raise this error, but webhook still set successfully.
    except telepot.exception.TooManyRequestsError:
        pass

    webhook.run_as_thread()
