from telebot import TeleBot
from keep_alive import keep_alive
import requests
import time


keep_alive()

BASE_URL = "https://pastebin.com/raw/BdJYWtGw"
CALL_URL = "https://sms-call.vercel.app/api/call"
MSG_URL = "https://spamwhats.vercel.app/"

BOT_TOKEN = '6552877762:AAFQnohFxwTJylt3Xx6UuqybUiti--2HARs'

bot = TeleBot(BOT_TOKEN)

stop_spam = False

# Handle the '/start' command


@bot.message_handler(commands=['start'])
def send_welcome(message):
    chat_id = message.chat.id
    user_name = message.chat.first_name if message.chat.first_name else "User"
    welcome_message = f"Welcome, {user_name}.\nServer is running"
    bot.send_message(chat_id, welcome_message, parse_mode="HTML")
# Handle the '/spamcall' command
@bot.message_handler(commands=['spamcall'])
def spam_call(message):
    global stop_spam
    chat_id = message.chat.id
    response = requests.get(BASE_URL)
    phone_numbers = response.text.splitlines()

    for phone_number in phone_numbers:
        if stop_spam:
            stop_spam = False
            return
        payload = {"phone": phone_number}
        try:
            response = requests.post(CALL_URL, json=payload)
            if response.status_code == 200:
                success_message = f"Call made to {phone_number} successfully"
                bot.send_message(chat_id, success_message, parse_mode="HTML")
            else:
                error_message = f"Failed{phone_number}. Status code: {response.status_code}"
                bot.send_message(chat_id, error_message, parse_mode="HTML")
        except requests.exceptions.RequestException as e:
            error_message = f"Error occurred while making call to {phone_number}: {e}"
            bot.send_message(chat_id, error_message, parse_mode="HTML")
        time.sleep(3)
        
# Handle the '/spammsg' command
@bot.message_handler(commands=['spammsg'])
def spam_message(message):
    chat_id = message.chat.id
    global stop_spam
    response = requests.get(BASE_URL)
    phone_numbers = response.text.splitlines()
    for phone_number in phone_numbers:
        if stop_spam:
            stop_spam = False
            return
        try:
            response2 = requests.get(f'{MSG_URL}send_spam?number={phone_number}')
            if response2.status_code == 200:
                success_message = f"Message sent to {phone_number} successfully"
                bot.send_message(chat_id, success_message,parse_mode="HTML")
            else:
                error_message = f"Failed {phone_number}. Status code: {response2.status_code}"
                bot.send_message(chat_id, error_message, parse_mode="HTML")
        except requests.exceptions.RequestException as e:
            error_message = f"Error occurred while sending WhatsApp message to {phone_number}: {e}"
            bot.send_message(chat_id, error_message, parse_mode="HTML")
        time.sleep(5)


@bot.message_handler(commands=['stop'])
def stop_spam_command(message):
    chat_id = message.chat.id
    global stop_spam
    stop_spam = True
    bot.send_message(chat_id, 'Spam stopped successfully!')


bot.polling()
