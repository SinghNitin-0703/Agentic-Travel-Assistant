from app.schemas import HotelSearchParams, HotelOffer
from app.client import serpapi_request

async def search_hotels(
    city: str,
    check_in: str,
    check_out: str,
    adults: int = 2,
    max_price_per_night: float = None,
    currency: str = "INR",
) -> str:
    """
    Search for hotels using SerpAPI Google Hotels.

    Args:
        city: City name for the hotel search (e.g., 'Jaipur', 'Goa', 'Manali').
        check_in: Check-in date in YYYY-MM-DD format.
        check_out: Check-out date in YYYY-MM-DD format.
        adults: Number of adult guests (1-9, default 2).
        max_price_per_night: Optional maximum price per night filter.
        currency: Currency code (default 'INR').

    Returns:
        A formatted string listing hotel options, or an error message.
    """
    print(f"  TOOL CALLED: search_hotels({city}, {check_in} to {check_out})")

    try:
        params = HotelSearchParams(
            query=f"hotels in {city}",
            check_in=check_in,
            check_out=check_out,
            adults=adults,
            max_price_per_night=max_price_per_night,
            currency=currency,
        )

        api_params = {
            "engine": "google_hotels",
            "q": params.query,
            "check_in_date": params.check_in.isoformat(),
            "check_out_date": params.check_out.isoformat(),
            "adults": str(params.adults),
            "currency": params.currency,
            "gl": "in",
            "hl": "en",
        }

        response = await serpapi_request(api_params)
        raw_properties = response.get("properties", [])

        if not raw_properties:
            return f"No hotels found in {city} for the given dates. Try different dates or a nearby city."

        nights = (params.check_out - params.check_in).days
        if nights <= 0:
            nights = 1

        offers = []
        for idx, raw in enumerate(raw_properties):
            try:
                rate_per_night = raw.get("rate_per_night", {})
                total_rate = raw.get("total_rate", {})

                per_night_str = rate_per_night.get("lowest", "0") if isinstance(rate_per_night, dict) else str(rate_per_night)
                total_str = total_rate.get("lowest", "0") if isinstance(total_rate, dict) else str(total_rate)

                per_night_clean = ''.join(c for c in per_night_str if c.isdigit() or c == '.')
                total_clean = ''.join(c for c in total_str if c.isdigit() or c == '.')

                per_night_val = float(per_night_clean) if per_night_clean else 0
                total_val = float(total_clean) if total_clean else per_night_val * nights

                if per_night_val == 0 and total_val > 0:
                    per_night_val = total_val / nights

                amenities = raw.get("amenities", [])
                if not amenities:
                    amenities = []

                offer = HotelOffer(
                    hotel_id=f"HTL-{idx+1:03d}",
                    hotel_name=raw.get("name", "Unknown Hotel"),
                    star_rating=raw.get("overall_rating"),
                    price_per_night=per_night_val,
                    total_price=total_val,
                    currency=params.currency,
                    amenities=amenities[:5] if isinstance(amenities, list) else [],
                    link=raw.get("link"),
                    property_token=raw.get("serpapi_property_details_link", "").split("property_token=")[-1].split("&")[0] if raw.get("serpapi_property_details_link") else None,
                )

                if params.max_price_per_night and offer.price_per_night > params.max_price_per_night:
                    continue
                offers.append(offer)
            except Exception:
                continue

        offers.sort(key=lambda o: o.price_per_night)
        top_offers = offers[:5]

        if not top_offers:
            return f"No hotels found under {max_price_per_night} {currency}/night in {city}."

        results = []
        for i, offer in enumerate(top_offers, 1):
            stars = f"{offer.star_rating}⭐" if offer.star_rating else "N/A"
            amenities_str = ", ".join(offer.amenities) if offer.amenities else "Not listed"
            results.append(
                f"**Option {i}:** {offer.hotel_name} ({stars})\n"
                f"  💰 Per Night: **{offer.price_per_night:,.0f} {offer.currency}**\n"
                f"  💰 Total ({nights} nights): {offer.total_price:,.0f} {offer.currency}\n"
                f"  🏨 Amenities: {amenities_str}\n"
                f"  🆔 Hotel ID: `{offer.hotel_id}`"
            )

        return f" **Hotel Results in {city} ({nights} nights):**\n\n" + "\n\n".join(results)

    except Exception as e:
        return f" Error searching hotels: {str(e)}"

async def get_hotel_details(
    hotel_name: str,
    city: str,
    check_in: str,
    check_out: str,
    adults: int = 2,
    currency: str = "INR",
) -> str:
    """
    Get detailed information about a specific hotel.

    Args:
        hotel_name: The name of the hotel to look up.
        city: The city where the hotel is located.
        check_in: Check-in date in YYYY-MM-DD format.
        check_out: Check-out date in YYYY-MM-DD format.
        adults: Number of adult guests.
        currency: Currency code (default 'INR').

    Returns:
        Detailed hotel information string.
    """
    print(f"  TOOL CALLED: get_hotel_details({hotel_name} in {city})")

    try:
        api_params = {
            "engine": "google_hotels",
            "q": f"{hotel_name} {city}",
            "check_in_date": check_in,
            "check_out_date": check_out,
            "adults": str(adults),
            "currency": currency,
            "gl": "in",
            "hl": "en",
        }

        response = await serpapi_request(api_params)
        properties = response.get("properties", [])

        if not properties:
            return f"Could not find details for '{hotel_name}' in {city}."

        raw = properties[0]
        name = raw.get("name", hotel_name)
        rating = raw.get("overall_rating", "N/A")
        reviews = raw.get("reviews", "N/A")
        hotel_class = raw.get("hotel_class", "")
        description = raw.get("description", "No description available.")
        amenities = raw.get("amenities", [])

        rate_per_night = raw.get("rate_per_night", {})
        per_night_str = rate_per_night.get("lowest", "N/A") if isinstance(rate_per_night, dict) else str(rate_per_night)

        nearby = raw.get("nearby_places", [])
        nearby_str = ""
        if nearby:
            nearby_items = []
            for p in nearby[:5]:
                t_name = p.get("name", "Unknown")
                t_dist = p.get("transportations", [{}])
                dist_text = ""
                if t_dist and isinstance(t_dist, list) and len(t_dist) > 0:
                    dist_text = f" ({t_dist[0].get('duration', '')})"
                nearby_items.append(f"    • {t_name}{dist_text}")
            nearby_str = "\n  📍 **Nearby Places:**\n" + "\n".join(nearby_items)

        amenities_str = ", ".join(amenities[:8]) if amenities else "Not listed"

        return (
            f"🏨 **{name}** {hotel_class}\n"
            f"  ⭐ Rating: {rating}/5 ({reviews} reviews)\n"
            f"  💰 Price: **{per_night_str}** per night\n"
            f"  📝 {description}\n"
            f"  🏊 Amenities: {amenities_str}"
            f"{nearby_str}"
        )

    except Exception as e:
        return f" Error fetching hotel details: {str(e)}"
