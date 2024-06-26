import os
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from googleapiclient.discovery import build
import logging

# Configurar logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Claves de API
TELEGRAM_API_KEY = '7382427066:AAGHHDfmMd6llYa5CuI__iEx1e1gqiUp-Ws'
YOUTUBE_API_KEY = 'AIzaSyC455HeCuodHQprSrcfYraCQThuyY3Kl14'

# Configurar la API de YouTube
youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

# Función para el comando /start
def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hola {user.mention_markdown_v2()}\! Bienvenido a Tapconcoin\.',
        reply_markup=ForceReply(selective=True),
    )

# Función para manejar mensajes de texto
def echo(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(update.message.text)

# Función para obtener el número de suscriptores de un canal de YouTube
def get_subscribers():
    request = youtube.channels().list(
        part="statistics",
        id="UC3dYlWkXVzfx9AsYoNn0tBQ"
    )
    response = request.execute()
    return response["items"][0]["statistics"]["subscriberCount"]

# Función para el comando /subscribers
def subscribers(update: Update, context: CallbackContext) -> None:
    subscriber_count = get_subscribers()
    update.message.reply_text(f"El canal tiene {subscriber_count} suscriptores.")

# Función principal para iniciar el bot
def main() -> None:
    # Crear el Updater y pasarle el token del bot
    updater = Updater(TELEGRAM_API_KEY)

    # Obtener el dispatcher para registrar los manejadores
    dispatcher = updater.dispatcher

    # Registrar manejadores de comandos
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("subscribers", subscribers))

    # Registrar manejador de mensajes de texto
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Iniciar el bot
    updater.start_polling()

    # Correr el bot hasta que se detenga con Ctrl-C
    updater.idle()

if __name__ == '__main__':
    main()

