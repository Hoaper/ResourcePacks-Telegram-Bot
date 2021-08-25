from bs4 import BeautifulSoup
import requests
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from time import sleep

# temp
from pprint import pprint

# CVARS
smtp_login = os.environ.get("P_LOGIN")
smtp_passwd = os.environ.get("P_PASSWD")


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

class On_change_handler:

	def html2gmail_processor(self, body: list):

		urls = []
		for part in body:

			part = part.a
			url = part['href']
			image = "https://pvprp.com/" + part.find(class_="recent-banner")['style'].split('"')[1]

			urls.append(url)
			urls.append(image)

		sending = Mail()
		sending.sendUrls(urls)
		print(f"[=>] {urls[0]}")
		return




	def checkChanges(self):
		
		while True:
			# sleep(5*60)
			
			rawText = requests.get('https://pvprp.com/').text
			soup = BeautifulSoup(rawText, 'html.parser')

			new_six_rp = soup.find_all('div', class_="recent-in-grid")[:6]
			# new_six_rp[0].contents[1].a['href']="https://pvprp.com/pack?p=1145" # testing
			if new_six_rp == self.old_six_rp:
				# Old rps replaced by new rps
				# => skip
				self.old_six_rp = new_six_rp
				continue
			else:

				# DELETING ALL OLD RESOURCEPACKS FROM new_six_rp
				changes = []
				
				for new_rp in new_six_rp:

					if new_rp in self.old_six_rp:
						pass
					else:
						changes.append(new_rp)

				self.old_six_rp = new_six_rp

				self.html2gmail_processor(changes)

	def __init__(self):
		
		print("Handler started")

		rawText = requests.get('https://pvprp.com/').text
		soup = BeautifulSoup(rawText, 'html.parser')

		self.old_six_rp = soup.find_all('div', class_="recent-in-grid")[:6]
		self.checkChanges()


hdler = On_change_handler()
