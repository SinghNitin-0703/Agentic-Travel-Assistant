from app.schemas import FlightSearchParams, FlightOffer
from app.client import serpapi_request

CABIN_CLASS_MAP = {
    "economy": 1,
    "premium_economy": 2,
    "business": 3,
    "first": 4,
}

async def search_flights(
    origin: str,
    destination: str,
    departure_date: str,
    return_date: str = None,
    cabin_class: str = "economy",
    adults: int = 1,
    max_price: float = None,
    currency: str = "INR",
) -> str:
    """
    Search for flights using SerpAPI Google Flights.

    Args:
        origin: 3-letter IATA airport code for departure (e.g., 'DEL', 'BOM', 'BLR').
        destination: 3-letter IATA airport code for arrival (e.g., 'GOI', 'JAI', 'CCU').
        departure_date: Departure date in YYYY-MM-DD format.
        return_date: Optional return date in YYYY-MM-DD format for round-trip.
        cabin_class: Cabin class — one of 'economy', 'premium_economy', 'business', 'first'.
        adults: Number of adult passengers (1-9).
        max_price: Optional maximum total price filter in the given currency.
        currency: Currency code for prices (default 'INR').

    Returns:
        A formatted string listing the top 5 flight offers, or an error message.
    """
    print(f"  TOOL CALLED: search_flights({origin} → {destination}, {departure_date})")

    try:
        trip_type = 1 if return_date else 2
        params = FlightSearchParams(
            origin=origin.upper(),
            destination=destination.upper(),
            departure_date=departure_date,
            return_date=return_date,
            trip_type=trip_type,
            cabin_class=cabin_class,
            adults=adults,
            max_price=max_price,
            currency=currency,
        )

        # Build SerpAPI request
        api_params = {
            "engine": "google_flights",
            "departure_id": params.origin,
            "arrival_id": params.destination,
            "outbound_date": params.departure_date.isoformat(),
            "type": str(params.trip_type),
            "currency": params.currency,
            "hl": "en",
            "gl": "in",
            "adults": str(params.adults),
            "travel_class": str(CABIN_CLASS_MAP.get(params.cabin_class, 1)),
        }
        if params.return_date:
            api_params["return_date"] = params.return_date.isoformat()

        response = await serpapi_request(api_params)

        best_flights = response.get("best_flights", [])
        other_flights = response.get("other_flights", [])
        all_flights = best_flights + other_flights

        if not all_flights:
            return "No flights found for the given route and date. Please try different dates or airports."

        offers = []
        for idx, flight_group in enumerate(all_flights):
            try:
                flights = flight_group.get("flights", [])
                if not flights:
                    continue

                first_leg = flights[0]
                last_leg = flights[-1]
                price = float(flight_group.get("price", 0))

                airlines = list(dict.fromkeys(leg.get("airline", "Unknown") for leg in flights))
                
                offer = FlightOffer(
                    flight_id=f"FL-{idx+1:03d}",
                    airline=", ".join(airlines),
                    departure_airport=first_leg.get("departure_airport", {}).get("id", params.origin),
                    arrival_airport=last_leg.get("arrival_airport", {}).get("id", params.destination),
                    departure_time=first_leg.get("departure_airport", {}).get("time", ""),
                    arrival_time=last_leg.get("arrival_airport", {}).get("time", ""),
                    total_price=price,
                    currency=params.currency,
                    stops=len(flights) - 1,
                    duration=str(flight_group.get("total_duration", "N/A")) + " min",
                )

                if params.max_price and offer.total_price > params.max_price:
                    continue
                offers.append(offer)
            except Exception:
                continue

        offers.sort(key=lambda o: o.total_price)
        top_offers = offers[:5]

        if not top_offers:
            return f"No flights found under your budget of {params.max_price} {params.currency}."

        results = []
        for i, offer in enumerate(top_offers, 1):
            stop_text = "Non-stop" if offer.stops == 0 else f"{offer.stops} stop(s)"
            results.append(
                f"**Option {i}:** {offer.airline}\n"
                f"  ✈️  {offer.departure_airport} → {offer.arrival_airport}\n"
                f"  🕐 Departure: {offer.departure_time}\n"
                f"  🕐 Arrival: {offer.arrival_time}\n"
                f"  ⏱️  Duration: {offer.duration}\n"
                f"  🔄 Stops: {stop_text}\n"
                f"  💰 Price: **{offer.total_price:,.0f} {offer.currency}**\n"
                f"  🆔 Flight ID: `{offer.flight_id}`"
            )

        return "✈️ **Flight Results:**\n\n" + "\n\n".join(results)

    except Exception as e:
        return f" Error searching flights: {str(e)}"
