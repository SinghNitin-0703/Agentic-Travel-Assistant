from datetime import datetime
from app.database import load_session, save_session

async def build_itinerary(
    session_id: str,
    flight_summary: str = None,
    hotel_summary: str = None,
    places_summary: str = None,
    total_flight_price: float = 0,
    total_hotel_price: float = 0,
    currency: str = "INR",
) -> str:
    """
    Build a travel itinerary combining selected flight, hotel, and places.

    This assembles the user's selected options into a clean itinerary
    summary and saves it to the SQLite session as a draft.

    Args:
        session_id: The current session UUID.
        flight_summary: A text summary of the selected flight details.
        hotel_summary: A text summary of the selected hotel details.
        places_summary: A text summary of recommended places to visit.
        total_flight_price: The price of the selected flight.
        total_hotel_price: The total hotel price.
        currency: Currency code (default 'INR').

    Returns:
        A formatted string showing the complete draft itinerary.
    """
    print(f"  TOOL CALLED: build_itinerary(flight={flight_summary is not None}, hotel={hotel_summary is not None})")

    try:
        total_price = total_flight_price + total_hotel_price

        session = await load_session(session_id)
        itinerary_data = {
            "flight_summary": flight_summary,
            "hotel_summary": hotel_summary,
            "places_summary": places_summary,
            "total_flight_price": total_flight_price,
            "total_hotel_price": total_hotel_price,
            "total_price": total_price,
            "currency": currency,
            "status": "draft",
            "created_at": datetime.now().isoformat(),
        }
        session["itinerary"] = itinerary_data
        await save_session(session_id, session)

        sections = [" **Draft Itinerary — Bharat YatraBot** 🇮🇳"]

        if flight_summary: sections.append(f"✈️ **Flight:**\n{flight_summary}")
        if hotel_summary: sections.append(f"🏨 **Hotel:**\n{hotel_summary}")
        if places_summary: sections.append(f"🗺️ **Places to Visit:**\n{places_summary}")

        sections.append(
            f"---\n"
            f"💰 **Estimated Grand Total: {total_price:,.0f} {currency}**\n"
            f"  ✈️ Flight: {total_flight_price:,.0f} {currency}\n"
            f"  🏨 Hotel: {total_hotel_price:,.0f} {currency}\n"
            f"📌 Status: DRAFT\n\n"
            f"Would you like to confirm this itinerary or make any changes?"
        )

        return "\n\n".join(sections)

    except Exception as e:
        return f" Error building itinerary: {str(e)}"
