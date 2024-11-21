from pydantic import BaseModel
from pydantic import Field

class Coordinates(BaseModel):
    lat: float = Field(description="Latitude coordinate")
    lon: float = Field(description="Longitude coordinate")