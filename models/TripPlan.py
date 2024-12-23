from typing import List
from models.Trip import Trip
from pydantic import BaseModel

class TripPlan(BaseModel):
    destinations: List[Trip]