from dotenv import load_dotenv

load_dotenv()
from data_manager import DataManager
import requests_cache
from pprint import pprint
from flight_search import FlightSearch
from datetime import datetime, timedelta
from flight_data import find_cheapest_flight
from notification_manager import NotificationManager

# import json

requests_cache.install_cache(
    "flight_cache",
    urls_expire_after={
        "*.sheety.co*": requests_cache.DO_NOT_CACHE,
        "*": 3600,
    },
)
datamanager = DataManager()
flightsearch = FlightSearch()
notification = NotificationManager()

sheet_data = datamanager.sheet_data
user_data = datamanager.customer_emails
tomorrow = datetime.now() + timedelta(days=1)
after_six_mo = datetime.now() + timedelta(days=(6 * 30))

emails = []

for customer in user_data:
    emails.append(customer["whatIsYourEmail?"])

for destination in sheet_data:
    if destination["iataCode"] == "DEL":
        continue

    print(f"Getting direct flights for {destination['city']}... for each destination")
    direct_flights = flightsearch.flight(
        origin_city_code="DEL",
        destination_city_code=destination["iataCode"],
        from_time=tomorrow,
        to_time=after_six_mo,
        is_direct=True,
    )

    if not direct_flights["best_flights"] and not direct_flights["other_flights"]:
        print(
            f"No direct flight to {destination['city']}. Looking for indirect flights..."
        )

        direct_flights = flightsearch.flight(
            origin_city_code="DEL",
            destination_city_code=destination["iataCode"],
            from_time=tomorrow,
            to_time=after_six_mo,
            is_direct=False,
        )

    cheapest_flight = find_cheapest_flight(
        direct_flights, after_six_mo.strftime("%Y-%m-%d")
    )

    
    if (
        cheapest_flight.price != "N/A"
        and cheapest_flight.price < destination["lowestPrice"]
    ):

        datamanager.update_lowest_price(
            row_id=destination["id"], new_price=cheapest_flight.price
        )

        if cheapest_flight.stops == 0:
            message = (
                f"Subject:Low Price Alert!\n\n"
                f"Only GBP{cheapest_flight.price} to fly from "
                f"{cheapest_flight.origin_airport} to "
                f"{cheapest_flight.destination_airport}.\n"
                f"Departure: {cheapest_flight.out_date}\n"
                f"Return: {cheapest_flight.return_date}"
            )
        else:
            message = (
                f"Subject:Low Price Alert!\n\n"
                f"Only GBP{cheapest_flight.price} to fly from "
                f"{cheapest_flight.origin_airport} to "
                f"{cheapest_flight.destination_airport}.\n"
                f"Departure: {cheapest_flight.out_date}\n"
                f"Return: {cheapest_flight.return_date}\n"
                f"Flight has {cheapest_flight.stops} stop(s)."
            )

        notification.send_emails(emails, message)

    #     message = (
    #         f"Low price alert!\n\n"
    #         f"Only £{cheapest_flight.price} to fly from "
    #         f"{cheapest_flight.origin_airport} to "
    #         f"{cheapest_flight.destination_airport}.\n\n"
    #         f"Departure: {cheapest_flight.out_date}\n"
    #         f"Return: {cheapest_flight.return_date}"
    #     )
    #     notification.send_noti(message)
