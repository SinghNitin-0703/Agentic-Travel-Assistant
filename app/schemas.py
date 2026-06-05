from datetime import date
from typing import List, Optional, Literal
from pydantic import BaseModel, Field

# Input Schemas
class FlightSearchParams(BaseModel):
    """Parameters for searching flights via SerpAPI Google Flights."""
    origin: str = Field(..., min_length=3, max_length=3, description="IATA airport code, e.g. 'DEL'")
    destination: str = Field(..., min_length=3, max_length=3, description="IATA airport code, e.g. 'GOI'")
    departure_date: date = Field(..., description="Departure date in YYYY-MM-DD format")
    return_date: Optional[date] = Field(None, description="Return date for round-trip (None for one-way)")
    trip_type: int = Field(2, ge=1, le=3, description="1=Round trip, 2=One way, 3=Multi-city")
    cabin_class: Literal["economy", "premium_economy", "business", "first"] = "economy"
    adults: int = Field(1, ge=1, le=9, description="Number of adult passengers")
    max_price: Optional[float] = Field(None, ge=0, description="Maximum total price filter")
    currency: str = Field("INR", description="Currency code for price display")

class HotelSearchParams(BaseModel):
    """Parameters for searching hotels via SerpAPI Google Hotels."""
    query: str = Field(..., description="Search query, e.g. 'hotels in Jaipur'")
    check_in: date = Field(..., description="Check-in date")
    check_out: date = Field(..., description="Check-out date")
    adults: int = Field(2, ge=1, le=9)
    max_price_per_night: Optional[float] = Field(None, ge=0)
    currency: str = "INR"

class PlaceSearchParams(BaseModel):
    """Parameters for searching tourist places via SerpAPI Google Maps."""
    query: str = Field(..., description="What to search for, e.g. 'tourist attractions'")
    location: str = Field(..., description="City or area name, e.g. 'Udaipur'")

# Output Schemas
class FlightOffer(BaseModel):
    """Validated flight offer from SerpAPI Google Flights."""
    flight_id: str
    airline: str
    departure_airport: str = ""
    arrival_airport: str = ""
    departure_time: str
    arrival_time: str
    total_price: float
    currency: str
    stops: int
    duration: Optional[str] = None

class HotelOffer(BaseModel):
    """Validated hotel offer from SerpAPI Google Hotels."""
    hotel_id: str
    hotel_name: str
    star_rating: Optional[float] = None
    price_per_night: float
    total_price: float
    currency: str
    amenities: List[str] = []
    link: Optional[str] = None
    property_token: Optional[str] = None

class PlaceResult(BaseModel):
    """Validated place result from SerpAPI Google Maps."""
    name: str
    address: Optional[str] = None
    rating: Optional[float] = None
    reviews_count: Optional[int] = None
    place_type: Optional[str] = None
    description: Optional[str] = None

class Itinerary(BaseModel):
    """Complete travel itinerary combining flight, hotel, and places."""
    session_id: str
    flight: Optional[FlightOffer] = None
    hotel: Optional[HotelOffer] = None
    places: List[PlaceResult] = []
    total_price: float = 0.0
    currency: str = "INR"
    status: Literal["draft", "confirmed"] = "draft"
