import telebot
import os
import t_mail
from t_mail import channel
from subprocess import Popen, PIPE

TOKEN = os.environ.get("TGM_TOKEN")

# TELEGRAM CVARS


bot = telebot.TeleBot(TOKEN)

print(f"Connected successfully!")

@bot.message_handler(commands=['start'])
def welcome(message):
	if str(channel) == '':
		channel.change(str(message.chat.id))
		print(f'[+] {message.chat.id}')
		bot.send_message(channel, "Handler started")
	
	else:
		bot.send_message(message.chat.id, "Bot already handle messages from other group")


	handling()


@bot.message_handler(commands=["print"])
def printChatId(message):

	print(channel)


def handling():
	
	while True:
		handle = t_mail.Mail().returnBody()
		print(handle)

bot.polling()

