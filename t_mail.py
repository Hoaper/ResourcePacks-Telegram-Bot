# NOT A CONFIG FILE, JUST TEMPLATES
import imaplib, email, telebot, os, sys
from t_bot import sendMessage, sendPhoto

TOKEN = os.environ.get("TGM_TOKEN")

## CVARS
# Global variable - channel

# GMAIL CVARS
m_host = "imap.gmail.com"
m_user = os.environ.get("MAIL_LOGIN")
m_passwd = os.environ.get("MAIL_PASSWD")



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
		
		sendPhoto(self.channel, url)

	def sendMessage(self, url):
		
		sendMessage(self.channel, "\n".join(url))

	def __init__(self, channel):
		self.channel = channel
		client = self.getClient(m_host, m_user, m_passwd)
		while True:
			try:
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

								for line in body_lines:
									if 'assets' in line:
										photo_lines.append(line)
									else:
										lines.append(line)

								self.sendMessage(lines)

								for photo_line in photo_lines:
									self.sendPhoto(photo_line)
			except imaplib.abort:
				client = self.getClient(m_host, m_user, m_passwd)


hdler = Mail(sys.argv[1])
