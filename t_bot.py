import telebot
import os
from subprocess import Popen, PIPE

TOKEN = os.environ.get("TGM_TOKEN")

# TELEGRAM CVARS


bot = telebot.TeleBot(TOKEN)

print(f"Telegram connected successfully!")

handled = False

@bot.message_handler(commands=['handle'])
def handle(message):
	if not handled:
		channel = str(message.chat.id)
		print(f'[+] {message.chat.id}')
		bot.send_message(channel, "Handler started")
	
		handled = True
		handling(channel)


@bot.message_handler(commands=["print"])
def printChatId(message):

	bot.send_message(message.chat.id, channel)


def handling(channel):
	
	Popen(['python', 't_mail.py', channel])

bot.polling()

