from pydantic import BaseModel, Field
from typing import Optional, List


class TideGaugeStation(BaseModel):
    id: str = Field(..., alias="@id")
    label: Optional[str] = None
    notation: Optional[str] = None
    easting: Optional[float] = None
    northing: Optional[float] = None
    lat: Optional[float] = None
    long: Optional[float] = None
    town: Optional[str] = None
    # Additional fields based on documentation and common API patterns
    description: Optional[str] = None
    status: Optional[str] = None
    measures: Optional[List[dict]] = None  # Assuming measures might be a list of dicts


class TideGaugeReading(BaseModel):
    id: str = Field(..., alias="@id")
    dateTime: Optional[str] = None
    measure: Optional[str] = None
    value: Optional[float] = None
    # Additional fields based on documentation and common API patterns
    unit: Optional[str] = None
