import telebot
import os
from subprocess import Popen, PIPE

TOKEN = os.environ.get("TGM_TOKEN")
secret_key = os.environ.get("TGM_KEY")
bot = telebot.TeleBot(TOKEN)

print(f"Telegram connected successfully!")

@bot.message_handler(commands=['handle'])
def handle(message):
	try:
		msg_arg = message.text.split(" ")[1]
		if msg_arg == secret_key
			channel = str(message.chat.id)
			print(f'[+] {message.chat.id}')
			bot.send_message(channel, "Handler started")

			handling(channel)
		
	except Exception:
		
		bot.send_message(message.chat.id, "Auth failure")


@bot.message_handler(commands=["print"])
def printChatId(message):

	bot.send_message(message.chat.id, channel)


def handling(channel):
	
	Popen(['python', 't_mail.py', channel])

bot.polling()

