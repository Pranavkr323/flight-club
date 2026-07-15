import requests
import os


SHEET_ENDPOINT = os.getenv("SHEET_ENDPOINT")
USERS_ENDPOINT = os.getenv("USERS_ENDPOINT")

class DataManager:
    def __init__(self):
        self.sheet_data = self.get_sheet_data()
        self.customer_emails = self.get_customer_emails()

    def get_sheet_data(self):
        sheet_response = requests.get(url=SHEET_ENDPOINT)
        sheet_response.raise_for_status()
        data = sheet_response.json()
        return data["sheet1"]

    def update_lowest_price(self, row_id, new_price):
        url = f"{SHEET_ENDPOINT}/{row_id}"
        json_body = {"sheet1": {"lowestPrice": new_price}}
        sheet_put = requests.put(url=url, json=json_body)
        sheet_put.raise_for_status()

    def get_customer_emails(self):
        users_emails = requests.get(url=USERS_ENDPOINT)
        users_emails.raise_for_status()
        user_data = users_emails.json()
        return user_data["users"]
