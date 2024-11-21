from models.Coordinates import Coordinates
from pydantic import BaseModel
from pydantic import Field

class Destination(BaseModel):
    coordinates: Coordinates
    name: str = Field(description="Destination port name")
    comfortLevel: str = Field(description="Comfort level of the sailor (Too Little Challenge, Comfortable Sailing, Moderate Sailing, Challenging Sailing, Extreme Sailing, Too Extreme to Sail)")
    distance: float = Field(description="Distance to the destination port in nautical miles")
    time: str = Field(description="Time duration to reach destination port from current location in hours (00:00)")

class DestinationList(BaseModel):
    destination1: Destination
    destination2: Destination
    destination3: Destination