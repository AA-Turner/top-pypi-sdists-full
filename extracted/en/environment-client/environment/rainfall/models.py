from pydantic import BaseModel, Field
from typing import Optional, List


class Station(BaseModel):
    id: str = Field(..., alias="@id")
    label: Optional[str] = None
    notation: Optional[str] = None
    easting: Optional[float] = None
    northing: Optional[float] = None
    lat: Optional[float] = None
    long: Optional[float] = None
    riverName: Optional[str] = None
    town: Optional[str] = None
    # Additional fields based on common API patterns and Rainfall API description
    description: Optional[str] = None
    status: Optional[str] = None
    measures: Optional[List[dict]] = None  # Assuming measures might be a list of dicts


class Measure(BaseModel):
    id: str = Field(..., alias="@id")
    label: Optional[str] = None
    notation: Optional[str] = None
    parameter: Optional[str] = None
    parameterName: Optional[str] = None
    qualifier: Optional[str] = None
    unitName: Optional[str] = None
    station: Optional[str] = None
    # Additional fields based on common API patterns and Rainfall API description
    description: Optional[str] = None
    unit: Optional[str] = None


class Reading(BaseModel):
    id: str = Field(..., alias="@id")
    dateTime: Optional[str] = None
    measure: Optional[str] = None
    value: Optional[float] = None
    # Additional fields based on common API patterns and Rainfall API description
    unit: Optional[str] = None
