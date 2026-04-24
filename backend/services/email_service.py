import os
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_cold_email(to_email: str, subject: str, body: str) -> bool:
    gmail_address = os.getenv("GMAIL_ADDRESS")
    gmail_password = os.getenv("GMAIL_APP_PASSWORD")

    if not gmail_address or not gmail_password:
        raise Exception("GMAIL_ADDRESS or GMAIL_APP_PASSWORD not set in environment")

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = gmail_address
    msg["To"] = to_email

    # Plain text only — HTML triggers spam filters for cold email
    msg.attach(MIMEText(body, "plain"))

    context = ssl.create_default_context()
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(gmail_address, gmail_password)
            server.sendmail(gmail_address, to_email, msg.as_string())
        return True
    except smtplib.SMTPAuthenticationError:
        raise Exception("SMTP Authentication failed. Check GMAIL_ADDRESS and GMAIL_APP_PASSWORD.")
    except smtplib.SMTPException as e:
        raise Exception(f"SMTP Error: {str(e)}")
