from typing import List
from models.Trip import Trip
from pydantic import BaseModel
from pydantic import Field

class TripPlan(BaseModel):
    destinations: List[Trip]