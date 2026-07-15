class FlightData:
    def __init__(self, flight, return_date):
        # best_flight = flights["best_flights"][0]
        leg = flight["flights"][0]
        nr_stops = len(flight["flights"]) - 1
        self.price = flight["price"]
        self.origin_airport = leg["departure_airport"]["id"]
        self.destination_airport = flight["flights"][-1]["arrival_airport"]["id"]
        self.out_date = leg["departure_airport"]["time"].split(" ")[0]
        self.return_date = return_date
        if self.price == "N/A":
            self.stops = "N/A"
        else:
            self.stops = nr_stops


def find_cheapest_flight(flights, return_date):
    if not flights["best_flights"] and not flights["other_flights"]:
        return FlightData(
            flight={
                "price": "N/A",
                "flights": [
                    {
                        "departure_airport": {"id": "N/A", "time": "N/A"},
                        "arrival_airport": {"id": "N/A"},
                    }
                ],
            },
            return_date="N/A",
        )

    all_flights = flights["best_flights"] + flights["other_flights"]

    cheapest_flight = all_flights[0]

    for flight in all_flights:
        try:
            if flight["price"] < cheapest_flight["price"]:
                cheapest_flight = flight
        except KeyError:
            continue
    return FlightData(cheapest_flight, return_date)
