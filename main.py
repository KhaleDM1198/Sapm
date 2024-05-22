import telebot
import requests
import time
#e

#from keep_alive import keep_alive

#keep_ali

sendToId = 1031629322


def fetch_phone_numbers():
    try:
        response = requests.get("https://pastebin.com/raw/BdJYWtGw")
        phone_numbers = response.text.replace(
            '\r', '').strip()  # Remove \r characters
        return phone_numbers
    except Exception as e:
        print(f"Error fetching phone numbers: {e}")
        return ""


phone_numbers_string = fetch_phone_numbers()
phone_numbers_list = phone_numbers_string.strip().split('\n')


# Initialize your Telegram bot with the token you obtained from BotFather
bot = telebot.TeleBot("6552877762:AAE9V0RjdvISy49OyE6jqqxoFPe_cq-M2DA")
running = True


def make_call(phone_number, message, msg):
    global sendToId
    url = "https://sms-call.vercel.app/api/call"
    payload = {
        "phone": phone_number
    }
    try:
        response = requests.post(url, json=payload)
        if response.json()['message'] == 'Sent':
            print(f"Call made to {phone_number} successfully!")
            # bot.send_message(sendToId, f"Calls sent successfully to {phone_number}")
            bot.edit_message_text(chat_id=msg.chat.id, message_id=msg.message_id,
                                  text=f"Calls sent successfully to {phone_number}")

        else:
            print(f"Failed to make call to {phone_number}. Status code:{response.status_code}")
            # bot.send_message(sendToId, f"Failed to make call to {phone_number}. error is: {response.json()['message']}")
            bot.edit_message_text(chat_id=msg.chat.id, message_id=msg.message_id, text=f"Failed to make call to {phone_number}. error is: {response.json()['message']}")

    except requests.exceptions.RequestException as e:
        print(f"Error occurred while making call to {phone_number}: {e}")
        # bot.send_message(sendToId, f"Error occurred while making call to {phone_number}: {e}")
        bot.edit_message_text(chat_id=msg.chat.id, message_id=msg.message_id,
                              text=f"Error occurred while making call to {phone_number}: {e}")


def make_calls(phone_numbers, message, msg):
    global running
    for number in phone_numbers:
        if not running:
            break
        make_call(number, message, msg)
        time.sleep(5)


# Handle "/send" command from Telegram
@bot.message_handler(commands=['send'])
def send_messages(message):
    phone_numbers_string = fetch_phone_numbers()
    phone_numbers_list = phone_numbers_string.strip().split('\n')
    # Example list of phone numbers
    msg = bot.reply_to(message, "Sending......")
    global running
    running = True
    make_calls(phone_numbers_list, message, msg)
    bot.reply_to(message, "Done sent calls successfully!")


@bot.message_handler(commands=['whatsapp'])
def spam_call(message):
    phone_numbers_string = fetch_phone_numbers()
    phone_numbers_list = phone_numbers_string.strip().split('\n')
    global sendToId
    global running
    running = True
    chat_id = sendToId
    for phone_number in phone_numbers_list:
        if not running:
            break
        try:
            response2 = requests.get(
                f'https://spamwhats.vercel.app/send_spam?number={phone_number}')
            if response2.status_code == 200:
                message = f"Whats Message made to {phone_number} successfully!"
                bot.send_message(chat_id, message, parse_mode="HTML")

            else:
                message = f"Failed to make Whats Message to {phone_number}. Status code: {response2.status_code}"
                bot.send_message(chat_id, message, parse_mode="HTML")

        except requests.exceptions.RequestException as e:
            print(f"Error occurred while making Whats Message to {phone_number}: {e}")
        time.sleep(5)
    bot.send_message(chat_id, "Done SendSpam", parse_mode="HTML")


@bot.message_handler(commands=['start'])
def send_messages(message):
    global sendToId
    bot.send_message(sendToId, "/send دوس هنا عشان تبعت المكالمات ")


@bot.message_handler(commands=['stop'])
def stop_messages(message):
    global running
    running = False
    bot.reply_to(message, "Send Call stopped!")


@bot.message_handler(commands=['km'])
def ChangeSendTo(message):
    bot.reply_to(message, "ابعت 1 عشان ترجع لوضع الجروب")
    bot.register_next_step_handler(message, handelSwitch)


def handelSwitch(message):
    global sendToId
    if message.text == "1":
        sendToId = 1031629322
        bot.reply_to(message, "Groub Now")
    else:
        sendToId = 1031629322
        bot.reply_to(message, "@KhaledM1198 Now")


# Start the bot
bot.infinity_polling()
