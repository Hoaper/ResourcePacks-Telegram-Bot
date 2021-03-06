import telebot
import os, signal
import asyncio
from t_mail import Mail

TOKEN = os.environ.get("TGM_TOKEN")
OWNER_ID = 1911939737
OWNER_ID = os.environ.get("OWNER_ID")
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def handle(message):
	try:
		if message.from_user.id == OWNER_ID:
			channel = str(message.chat.id)
			print(f'[+] {message.chat.id}')
			bot.send_message(channel, "Handler started")

			start(channel)
			

	except Exception as e:
		print(e)
		bot.send_message(message.chat.id, "Auth failure")


def start(chn):

	print(f"Telegram connected successfully!")
	Mail(chn, bot)
try:
	bot.polling(timeout=0)
except Exception as e:
	print(e)
	print("ERROR")
