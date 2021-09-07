# NOT A CONFIG FILE, JUST TEMPLATES

class Mail:
	
	def getClient(self, host, user, password): 
		import imaplib

		gmail = imaplib.IMAP4_SSL(host)
		
		gmail.login(user, password)

		return gmail

	def getUnreadMails(self, client):

		client.select("INBOX")
		sts, data = client.search(None, 'ALL', '(UNSEEN)')
		print(f'{sts} -> {data}')
		return data[0].split()

	def getMail(self, client, number: str):

		import email

		_, response = client.uid('fetch', number, '(RFC822)')
		response = response[0]
		
		return email.message_from_bytes(response)

	def sendPhoto(self, url):
		while True:
			try:

				self.bot.send_photo(int(self.channel), url)
			
			except Exception:
				pass

			else:
				break

	def sendMessage(self, url):
		
		self.bot.send_message(self.channel, "\n".join(url))

	def __init__(self, channel, bot):

		import os
		self.bot = bot

		## CVARS
		# Global variable - channel

		# GMAIL CVARS
		m_host = "imap.gmail.com"
		m_user = os.environ.get("MAIL_LOGIN")
		m_passwd = os.environ.get("MAIL_PASSWD")

		self.channel = channel
		client = self.getClient(m_host, m_user, m_passwd)
		while True:
			if 1==1:
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
			else:
				print(f"ERROR: {e}")
				client = self.getClient(m_host, m_user, m_passwd)
