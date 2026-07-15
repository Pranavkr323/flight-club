from twilio.rest import Client
import smtplib as smtp
import os


MY_EMAIL = os.getenv("MY_EMAIL")
MY_PASS = os.getenv("MY_PASS")

ACCOUNT_SID = os.getenv("ACCOUNT_SID")
AUTH_TOKEN = os.getenv("AUTH_TOKEN")

class NotificationManager:

    def __init__(self):
        self.client = Client(ACCOUNT_SID, AUTH_TOKEN)

    # def send_noti(self, message):
    #     whatsapp_message = self.client.messages.create(
    #         from_="whatsapp:+14155238886",
    #         body= message,
    #         to="whatsapp:+917004114961",
    #     )
    #     print(whatsapp_message.sid)

    def send_emails(self, to_addrs, message):
        with smtp.SMTP("smtp.gmail.com", port=587) as connection:
            connection.starttls()
            connection.login(user=MY_EMAIL, password=MY_PASS)
            connection.sendmail(from_addr=MY_EMAIL, to_addrs=to_addrs, msg=message)
