import discord as ds
from discord.ext import commands
## MAILING libs
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os

##needs to catch this from env
TOKEN = os.environ.get("DS_TOKEN")
smtp_login = os.environ.get("DS_LOGIN")
smtp_passwd = os.environ.get("DS_PASSWD")
##

allowed_channels = [790352654949285949,
					829743156533919814,
					879672565017227314]

bot = commands.Bot("\\")

## MAILING CLASS
class Mail:		

	def reAuth(self):

		self.server = smtplib.SMTP('smtp.gmail.com', 587)
		self.server.ehlo()
		self.server.starttls()
		self.server.ehlo()
		self.server.login(smtp_login, smtp_passwd)

	def createTemplate(self, body):
		template = MIMEMultipart('alternative')
		template['Subject'] = "resourcepack"
		template['From'] = smtp_login
		template['To'] = smtp_login
		template.attach(body)

		return template.as_string()

	def sendUrls(self, urls: list):

		# Body complition
		body = "\n".join(urls)
		body = MIMEText(body, "plain")
		template = self.createTemplate(body)
		self.reAuth()
		self.server.sendmail(smtp_login, smtp_login, template)

		self.server.quit()

@bot.event
async def on_message(msg):

	if msg.content.lower().startswith('https://pvprp.com'):

		if msg.channel.id in allowed_channels:

			urls = [msg.content] #1st - rp url, other - img urls
			files = msg.attachments

			for file in files:
				extension = file.filename.split(".")[-1]
				if extension in ["jpg", "jpeg", "png"]:
					urls.append(file.url)

			mail = Mail()
			mail.sendUrls(urls)

			print(f"[+] {urls[0]}")

		else:
			return

@bot.event
async def on_ready():
	print("[/] j7 connected successfully!")


bot.run(TOKEN)