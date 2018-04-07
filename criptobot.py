# -*- coding: utf-8 -*-
"""

"""

from telegram.ext import Updater, Filters, MessageHandler, CommandHandler
import logging
from functions import funcion1, funcion2
from threading import Thread
import time

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


# Mensaje en cuaquier caso
def echo(bot, update):
    texto = "Escriba /start mercado(BTC-ETH) intervalo(hour) para arrancar el bot."
    texto = texto + ' Escriba "/STOP" para parar (EMERGENCIA) ATENCION!'
    texto = texto + ' con /STOP sólo se podrá volver a iniciar desde el ordenador'
    bot.send_message(chat_id=update.message.chat_id, text=texto)

#  NO FUNCIONA
def stop(bot, update):
    texto = "Desconexión de emergencia del bot. No podrá realizar más acciones."
    bot.send_message(chat_id=update.message.chat_id, text=texto)
    #up.idle("SIGINT")
    
def start(bot, update, args):
    """ 
    Creamos un hilo por cada función para que se puedan ejecutar en paralelo
    """
    mercado = args[0] 
    intervalo = args[1]
    thread1 = Thread(target = funcion1, args = (mercado, intervalo, bot, update,))
    thread1.start()
    time.sleep(10) #Para asegurarnos que se ha actualizado el excel
    thread2 = Thread(target = funcion2, args = (mercado, intervalo, bot, update,))
    thread2.start()

def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)
    bot.send_message(chat_id=update.message.chat_id, text="Ha habido un error en el programa")
      
def main():  
    
    global token_tlgrm, id_conversacion, up
    token_tlgrm = '509446248:AAECtz3wUMKaa5d4TOEHmeQnvxBqA9Mb8YM'
    id_conversacion = 500840093
    
    up = Updater(token=token_tlgrm)#Diego 
    up.bot.send_message(chat_id=id_conversacion, text="Hola, el bot se acaba de iniciar.")
    up.dispatcher.add_handler(CommandHandler('STOP', stop))
    up.dispatcher.add_handler(CommandHandler('start', start, pass_args=True))
    up.dispatcher.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    up.dispatcher.add_error_handler(error)
    # Start the Bot
    up._clean_updates()
    up.start_polling()  
    # Block until you press Ctrl-C or the process receives SIGINT, SIGTERM or
    # SIGABRT. This should be used most of the time, since start_polling() is
    # non-blocking and will stop the bot gracefully.
    up.idle()
    
if __name__ == '__main__':
    main()
    
