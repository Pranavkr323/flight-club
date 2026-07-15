import requests
import os

SERP_ENDPOINT = os.getenv("SERP_ENDPOINT")

SERP_API_KEY = os.getenv("SERP_API_KEY")


class FlightSearch:
    def flight(
        self,
        origin_city_code,
        destination_city_code,
        from_time,
        to_time,
        is_direct=True,
    ):
        params = {
            "engine": "google_flights",
            "departure_id": origin_city_code,
            "arrival_id": destination_city_code,
            "outbound_date": from_time.strftime("%Y-%m-%d"),
            "return_date": to_time.strftime("%Y-%m-%d"),
            "type": "1",
            "adults": "1",
            "currency": "GBP",
            "api_key": SERP_API_KEY,
            "stops": 0 if is_direct else 1,
        }

        serp_response = requests.get(url=SERP_ENDPOINT, params=params)

        serp_response.raise_for_status()
        serp_data = serp_response.json()
        return serp_data
