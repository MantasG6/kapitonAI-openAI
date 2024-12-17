import datetime
from models.Coordinates import Coordinates
from pydantic import BaseModel
from pydantic import Field

class Trip(BaseModel):
    day: datetime.date = Field(description="Trip date in format YYYY-MM-DD")
    coordinates: Coordinates
    destination: str = Field(description="Destination port name")
    distanceNM: float = Field(description="Distance to the destination port in nautical miles")
    duration: str = Field(description="Time duration to reach destination port from current location in format HH:MM")
    comfortLevel: str = Field(description="Comfort level for the sailor according to his EXPERIENCE (Too Little Challenge, Comfortable Sailing, Moderate Sailing, Challenging Sailing, Extreme Sailing, Too Extreme to Sail)")
    safety: str = Field(description="Note about safety of the trip according to provided WEATHER and MARINE data")