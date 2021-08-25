# NOT A CONFIG FILE, JUST TEMPLATES
import imaplib, email, telebot, os

TOKEN = os.environ.get("TGM_TOKEN")

## CVARS
# Global variable - channel

# GMAIL CVARS
m_host = "imap.gmail.com"
m_user = os.environ.get("MAIL_LOGIN")
m_passwd = os.environ.get("MAIL_PASSWD")

class Variables:
	def __init__(self):
		self.channel = ''

	def __str__(self):
		return self.channel

	def change(self, channel):
		assert isinstance(channel, str)
		self.channel = channel

channel = Variables()

class Mail:
	
	def getClient(self, host, user, password): 
		
		gmail = imaplib.IMAP4_SSL(host)
		
		gmail.login(user, password)
		gmail.select('inbox')

		return gmail

	def getUnreadMails(self, client):

		result, data = client.uid('search', None, "UNSEEN")
		return data[0].split()

	def getMail(self, client, number: str):

		status, response = client.uid('fetch', number, '(RFC822)')
		response = response[0][1]
		
		return email.message_from_bytes(response)

	def sendPhoto(self, url):
		try:
			bot.send_photo(int(str(channel)), url)

		except Exception:
			self.sendPhoto(url)

	def __init__(self):
		while True:
			client = self.getClient(m_host, m_user, m_passwd)
			mail_nums = self.getUnreadMails(client)
			for mail_num in mail_nums:
				msg = self.getMail(client, mail_num)
				subject = msg.get("Subject")
				if subject == "resourcepack":
					for part in msg.walk():

						content_type = part.get_content_type()
						if content_type == "text/plain":
							body_lines = part.as_string().split("\n")
							breakline = body_lines.index('')
							body_lines = body_lines[breakline + 1:]

							lines = []
							photo_lines = []
							
							bot = telebot.TeleBot(TOKEN)
							
							for line in body_lines:
								if line.startswith('https://pvprp.com/'):
									lines.append(line)
								else:
									photo_lines.append(line)
							

							bot.send_message(int(str(channel)), "\n".join(lines))
							for photo_line in photo_lines:
								self.sendPhoto(photo_line)
			del bot
