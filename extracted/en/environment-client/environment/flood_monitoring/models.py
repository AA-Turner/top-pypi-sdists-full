from pydantic import BaseModel, Field
from typing import Optional


class FloodAreaInfo(BaseModel):
    id: str = Field(..., alias="@id")
    county: str
    notation: str
    polygon: str
    river_or_sea: str | None = Field(None, alias="riverOrSea")
    # Additional fields based on documentation
    label: Optional[str] = None
    description: Optional[str] = None


class FloodWarning(BaseModel):
    id: str = Field(..., alias="@id")
    description: str
    ea_area_name: str = Field(..., alias="eaAreaName")
    ea_region_name: str = Field(..., alias="eaRegionName")
    flood_area: FloodAreaInfo = Field(..., alias="floodArea")
    flood_area_id: str = Field(..., alias="floodAreaID")
    is_tidal: bool = Field(..., alias="isTidal")
    message: str
    severity: str
    severity_level: int = Field(..., alias="severityLevel")
    time_message_changed: str = Field(..., alias="timeMessageChanged")
    time_raised: str = Field(..., alias="timeRaised")
    time_severity_changed: str = Field(..., alias="timeSeverityChanged")
    # Additional fields based on documentation
    type: Optional[str] = None
    status: Optional[str] = None


class FloodArea(BaseModel):
    id: str = Field(..., alias="@id")
    county: str
    description: str
    ea_area_name: str = Field(..., alias="eaAreaName")
    flood_watch_area: str | None = Field(None, alias="floodWatchArea")
    fwd_code: str = Field(..., alias="fwdCode")
    label: str
    lat: float
    long: float
    notation: str
    polygon: str
    quick_dial_number: str = Field(..., alias="quickDialNumber")
    river_or_sea: str | None = Field(None, alias="riverOrSea")
    # Additional fields based on documentation
    type: Optional[str] = None


class MeasureInfo(BaseModel):
    id: str = Field(..., alias="@id")
    parameter: str
    parameter_name: str = Field(..., alias="parameterName")
    period: int
    qualifier: str
    unit_name: str = Field(..., alias="unitName")
    # Additional fields based on documentation
    label: Optional[str] = None
    description: Optional[str] = None


class Station(BaseModel):
    id: str = Field(..., alias="@id")
    rloi_id: str | list[str] | None = Field(None, alias="RLOIid")
    catchment_name: str | list[str] | None = Field(None, alias="catchmentName")
    date_opened: str | list[str] | None = Field(None, alias="dateOpened")
    easting: float | int | list[float] | list[int] | None = None
    label: str | list[str] | None = None
    lat: float | list[float] | None = None
    long: float | list[float] | None = None
    measures: list[MeasureInfo] | None = None
    northing: float | int | list[float] | list[int] | None = None
    notation: str
    river_name: str | None = Field(None, alias="riverName")
    stage_scale: str | None = Field(None, alias="stageScale")
    station_reference: str = Field(..., alias="stationReference")
    status: str | list[str] | None = Field(None, alias="status")
    town: str | None = Field(None, alias="town")
    wiski_id: str | None = Field(None, alias="wiskiID")
    datum_offset: float | int | str | None = Field(None, alias="datumOffset")
    downstage_scale: str | None = Field(None, alias="downstageScale")
    status_reason: str | None = Field(None, alias="statusReason")
    status_date: str | None = Field(None, alias="statusDate")
    type: str | None = Field(None, alias="type")
    # Additional fields based on documentation
    description: Optional[str] = None


class Reading(BaseModel):
    id: str = Field(..., alias="@id")
    date: str | None = None
    date_time: str = Field(..., alias="dateTime")
    measure: str
    value: float
    # Additional fields based on documentation
    unit: Optional[str] = None


class Measure(BaseModel):
    id: str = Field(..., alias="@id")
    datum_type: str | None = Field(None, alias="datumType")
    label: str
    latest_reading: Reading | None = Field(None, alias="latestReading")
    notation: str
    parameter: str
    parameter_name: str = Field(..., alias="parameterName")
    period: int | None = None
    qualifier: str
    station: str
    station_reference: str = Field(..., alias="stationReference")
    unit: str | None = None
    unit_name: str = Field(..., alias="unitName")
    value_type: str = Field(..., alias="valueType")
    # Additional fields based on documentation
    description: Optional[str] = None
