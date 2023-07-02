import os
import smtplib
import secrets
from email.mime.text import MIMEText
from email.header import Header
from utils import configs  # Configurações do GMAIL

class Email:
    def __init__(self):
        self.EMAIL_ADDRESS = configs.gmail  # GMAIL
        self.EMAIL_PASSWORD = configs.gmail_pass  # Senha do App

    def generate_token(self):
        token = secrets.token_urlsafe(16)
        return token

    def send_email(self, subject, body, dest):
        msg = MIMEText(body, 'html', 'utf-8')
        msg['Subject'] = Header(subject, 'utf-8')
        msg['From'] = self.EMAIL_ADDRESS
        msg['To'] = dest

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(self.EMAIL_ADDRESS, self.EMAIL_PASSWORD)
            smtp.sendmail(self.EMAIL_ADDRESS, dest, msg.as_string())

    def is_token_valid(self, token, token_valid):
        return token == token_valid
