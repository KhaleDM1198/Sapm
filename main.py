from telebot import TeleBot
from keep_alive import keep_alive
import requests
import time

keep_alive()
# Initialize the Telegram bot
bot = TeleBot('YOUR_TELEGRAM_BOT_TOKEN_HERE')
file_path = "doneee.csv"

# Handle the '/start' command
@bot.message_handler(commands=['start'])
def send_welcome(message):
    chat_id = message.chat.id
    user_name = message.chat.first_name if message.chat.first_name else "User"
    message = f"Welcome, {user_name}.\nServer is running"
    bot.send_message(chat_id, message, parse_mode="HTML")

# Handle the '/spamcall' command
@bot.message_handler(commands=['spamcall'])
def spam_call(message):
    chat_id = message.chat.id
    with open(file_path, 'r') as file:
        phone_numbers = file.read().splitlines()
        for phone_number in phone_numbers:
            url = "https://sms-call.vercel.app/api/call"
            payload = {
                "phone": phone_number
            }
            try:
                response = requests.post(url, json=payload)
                if response.status_code == 200:
                    message = f"Call made to {phone_number} successfully!"
                    bot.send_message(chat_id, message, parse_mode="HTML")
                else:
                    message = f"Failed to make call to {phone_number}. Status code: {response.status_code}"
                    bot.send_message(chat_id, message, parse_mode="HTML")
            except requests.exceptions.RequestException as e:
                print(f"Error occurred while making call to {phone_number}: {e}")
            time.sleep(5)

# Handle the '/spammsg' command
@bot.message_handler(commands=['spammsg'])
def spam_message(message):
    chat_id = message.chat.id
    with open(file_path, 'r') as file:
        phone_numbers = file.read().splitlines()
        for phone_number in phone_numbers:
            try:
                response = requests.get(f'https://spamwhats.vercel.app/send_spam?number={phone_number}')
                if response.status_code == 200:
                    message = f"Whats Message sent to {phone_number} successfully!"
                    bot.send_message(chat_id, message, parse_mode="HTML")
                else:
                    message = f"Failed to send Whats Message to {phone_number}. Status code: {response.status_code}"
                    bot.send_message(chat_id, message, parse_mode="HTML")
            except requests.exceptions.RequestException as e:
                print(f"Error occurred while sending Whats Message to {phone_number}: {e}")
            time.sleep(5)

bot.polling()
