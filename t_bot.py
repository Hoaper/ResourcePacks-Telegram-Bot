import telebot
import os, signal
from subprocess import Popen, PIPE

TOKEN = os.environ.get("TGM_TOKEN")
secret_key = os.environ.get("TGM_KEY")
bot = telebot.TeleBot(TOKEN)

print(f"Telegram connected successfully!")
global processes
processes = {}
@bot.message_handler(commands=['start'])
def handle(message):
	try:
		msg_arg = message.text.split(" ")[1]
		if msg_arg == secret_key:
			channel = str(message.chat.id)
			print(f'[+] {message.chat.id}')
			bot.send_message(channel, "Handler started")

			handling(channel)
		
	except Exception as e:
		print(e)
		bot.send_message(message.chat.id, "Auth failure")


@bot.message_handler(commands=["chatID"])
def printChatId(message):
	chat = message.chat.id

	bot.send_message(chat, chat)

@bot.message_handler(commands=["stop"])
def printChatId(message):

	try:
		pid = processes[message.chat.id]

	except Exception as e:
		print(e)
	
	os.kill(pid, signal.SIGTERM)
	bot.send_message(message.chat.id, "Stoped")

def handling(channel):
	
	process = Popen(['python', 't_mail.py', channel])
	processes[channel] = process.pid
bot.polling()

