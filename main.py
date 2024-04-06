from telebot import TeleBot
from keep_alive import keep_alive
import requests
import time

keep_alive()
# Initialize the Telegram bot
bot = TeleBot('6552877762:AAGoZjusMeGCJHe8istpXW8u5AFMhhFFL9c')
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
            # make_call(number)
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
                    return f"Failed to make call to {phone_number}. Status code: {response.status_code}"
            except requests.exceptions.RequestException as e:
                print(f"Error occurred while making call to {
                      phone_number}: {e}")
            time.sleep(5)


@bot.message_handler(commands=['spammsg'])
def spam_call(message):
    chat_id = message.chat.id
    with open(file_path, 'r') as file:
        phone_numbers = file.read().splitlines()
        for phone_number in phone_numbers:
            try:
                response2 = requests.get(
                    f'https://spamwhats.vercel.app/send_spam?number={phone_number}')
                if response2.status_code == 200:
                    message = f"Whats Message made to {
                        phone_number} successfully!"
                    bot.send_message(chat_id, message, parse_mode="HTML")

                else:
                    message = f"Failed to make Whats Message to {
                        phone_number}. Status code: {response2.status_code}"
                    bot.send_message(chat_id, message, parse_mode="HTML")

            except requests.exceptions.RequestException as e:
                print(f"Error occurred while making Whats Message to {
                      phone_number}: {e}")
            time.sleep(5)


bot.polling()
