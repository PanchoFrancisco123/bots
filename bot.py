import os
import random
import string
from instagram_private_api import Client
from instagram_private_api import errors
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

# Configuración del bot de Telegram
TOKEN_TELEGRAM = 'YOUR_TELEGRAM_BOT_TOKEN'
CHAT_ID = -1000000000  # ID del chat privado con el bot de Telegram

# Configuración de la cuenta de Instagram
INSTAGRAM_USERNAME = 'YOUR_INSTAGRAM_USERNAME'
INSTAGRAM_PASSWORD = 'YOUR_INSTAGRAM_PASSWORD'

# Número de bots a crear
NUM_BOTS = 300

# Comentario específico a likear
COMMENT_ID = 'SPECIFIC_COMMENT_ID'

def create_bot(profiles_folder):
    # Crea una cuenta de Instagram aleatoria
    username = f'bot_{random.randint(1000, 9999)}'
    password = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

    # Configura la cuenta de Instagram
    api = Client(username, password)
    api.login(INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD)

    # Guarda la configuración de la cuenta en el perfil
    profile_path = os.path.join(profiles_folder, username)
    os.makedirs(profile_path, exist_ok=True)
    with open(os.path.join(profile_path, 'config.json'), 'w') as f:
        f.write(api.session.auth_token)

    # Envía un mensaje al bot de Telegram indicando que el bot se ha creado correctamente
    message = f'Bot creado: @{username}'
    send_message_to_telegram(TOKEN_TELEGRAM, CHAT_ID, message)

    # Cierra la sesión de Instagram
    api.logout()

def send_message_to_telegram(token, chat_id, message):
    from telegram.ext import Updater
    updater = Updater(token, use_webhook=True)
    bot = updater.bot
    bot.sendMessage(chat_id=chat_id, text=message)

def like_comment():
    # Crea una instancia de Chrome con opciones de incognito
    options = Options()
    options.add_argument("--incognito")
    driver = webdriver.Chrome(options=options)

    # Inicia sesión en Instagram
    driver.get('https://www.instagram.com/')
    username_input = driver.find_element_by_name('username')
    username_input.send_keys(INSTAGRAM_USERNAME)
    password_input = driver.find_element_by_name('password')
    password_input.send_keys(INSTAGRAM_PASSWORD)
    password_input.send_keys(Keys.RETURN)

    # Busca el comentario específico y le da like
    driver.get(f'https://www.instagram.com/p/COMMENT_ID/')
    like_button = driver.find_element_by_xpath('//button[@class="fr66n"]')
    like_button.click()

    # Cierra la instancia de Chrome
    driver.close()

def main():
    profiles_folder = 'profiles'
    for i in range(NUM_BOTS):
        create_bot(profiles_folder)

    # Ejecuta el bot principal
    like_comment()

if __name__ == '__main__':
    main()
