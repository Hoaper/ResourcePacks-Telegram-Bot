import telebot
import os, signal
from subprocess import Popen, PIPE

TOKEN = os.environ.get("TGM_TOKEN")
bot = telebot.TeleBot(TOKEN)
secret_key = os.environ.get("TGM_KEY")

@bot.message_handler(commands=['start'])
def handle(message):
	try:
		if message.from_user.id == 1911939737:
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
def stop(message):

	try:
		pid = processes[str(message.chat.id)]

		os.kill(pid, signal.SIGTERM)
		bot.send_message(message.chat.id, "Stoped")

	except Exception as e:

		print(e)

def handling(channel):
	
	process = Popen(['python', 't_mail.py', channel])
	processes[channel] = process.pid

def sendMessage(channel, text):

	bot.send_message(channel, text)

def sendPhoto(channel, photo):

	try:

		bot.send_photo(int(channel), photo)
	except Exception:

		sendPhoto(photo)


def start():

	print(f"Telegram connected successfully!")
	global processes
	processes = {}

	bot.polling(timeout=0)

