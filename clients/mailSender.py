import smtplib
import os
from dotenv import load_dotenv

load_dotenv()
mailer_host = os.getenv('EMAIL_HOST')
mailer_port = int(os.getenv('EMAIL_PORT'))
username = os.getenv('USERNAME')
password = os.getenv('PASSWORD')


def send_email(email_from: str, email_to: str, body: str):
    message = f"""\
Subject: NewsList
To: {email_to}
From: {email_from}

{body}
"""

    with smtplib.SMTP(host=mailer_host, port=mailer_port) as srv:
        srv.login(username, password)
        srv.sendmail(email_from, email_to, message.encode("UTF-8"))

    return True