from app.schemas import PlaceSearchParams, PlaceResult
from app.client import serpapi_request

async def explore_places(
    query: str,
    location: str,
) -> str:
    """
    Discover tourist attractions, restaurants, temples, beaches, and more using Google Maps.

    Args:
        query: What to search for (e.g., 'tourist attractions', 'best restaurants',
               'temples', 'beaches', 'adventure activities', 'shopping markets').
        location: City or area in India (e.g., 'Goa', 'Jaipur', 'Varanasi', 'Munnar').

    Returns:
        A formatted string listing top places, or an error message.
    """
    print(f"  TOOL CALLED: explore_places('{query}' in '{location}')")

    try:
        params = PlaceSearchParams(query=query, location=location)

        api_params = {
            "engine": "google_maps",
            "q": f"{params.query} in {params.location}, India",
            "type": "search",
            "hl": "en",
            "gl": "in",
        }

        response = await serpapi_request(api_params)
        local_results = response.get("local_results", [])

        if not local_results:
            return f"No places found for '{query}' in {location}. Try a different search term."

        places = []
        for raw in local_results[:8]:
            try:
                place = PlaceResult(
                    name=raw.get("title", "Unknown Place"),
                    address=raw.get("address", ""),
                    rating=raw.get("rating"),
                    reviews_count=raw.get("reviews"),
                    place_type=raw.get("type", ""),
                    description=raw.get("description", ""),
                )
                places.append(place)
            except Exception:
                continue

        if not places:
            return f"Could not parse results for '{query}' in {location}."

        results = []
        for i, place in enumerate(places, 1):
            rating_str = f"{place.rating} ({place.reviews_count} reviews)" if place.rating else "No ratings"
            desc = f"\n   {place.description}" if place.description else ""
            place_type = f" — {place.place_type}" if place.place_type else ""
            results.append(
                f"**{i}. {place.name}**{place_type}\n"
                f"   {place.address or 'Address not available'}\n"
                f"   {rating_str}{desc}"
            )

        return f" **{query.title()} in {location}:**\n\n" + "\n\n".join(results)

    except Exception as e:
        return f" Error exploring places: {str(e)}"

async def explore_destinations(
    departure_city: str,
    currency: str = "INR",
) -> str:
    """
    Discover cheap flight destinations from a departure city using Google Travel Explore.

    Args:
        departure_city: IATA airport code of the departure city (e.g., 'DEL', 'BOM', 'BLR').
        currency: Currency code for price display (default 'INR').

    Returns:
        A formatted string listing popular/cheap destinations with prices.
    """
    print(f"🛠️  TOOL CALLED: explore_destinations(from {departure_city})")

    try:
        api_params = {
            "engine": "google_travel_explore",
            "departure_id": departure_city.upper(),
            "currency": currency,
            "hl": "en",
            "gl": "in",
        }

        response = await serpapi_request(api_params)

        destinations = response.get("destinations", [])
        if not destinations:
            destinations = response.get("flights_results", [])

        if not destinations:
            return f"No destination deals found from {departure_city}. Try a different departure city."

        results = []
        for i, dest in enumerate(destinations[:10], 1):
            city = dest.get("title", dest.get("city", "Unknown"))
            country = dest.get("country", "")
            price = dest.get("price", dest.get("flight_price", "N/A"))
            airport = dest.get("airport", {}).get("id", "") if isinstance(dest.get("airport"), dict) else ""

            location_str = f"{city}"
            if country:
                location_str += f", {country}"
            if airport:
                location_str += f" ({airport})"

            results.append(
                f"**{i}. {location_str}**\n"
                f"   From: **{price} {currency}**"
            )

        return f" **Destination Deals from {departure_city}:**\n\n" + "\n\n".join(results)

    except Exception as e:
        return f" Error exploring destinations: {str(e)}"
