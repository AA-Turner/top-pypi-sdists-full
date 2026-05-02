from typing import List, Optional
from datetime import datetime
from datamodel import BaseModel, Field
from .abstract import AbstractPayload


class EventPosition(BaseModel):
    """
    Event Position Model.
    """
    event_position_id: int = Field(primary_key=True, required=True)
    staff_position_id: int = Field(required=True)
    staff_position_name: str = Field(required=True)
    position_start_time: datetime = Field(required=True)
    position_end_time: datetime = Field(required=True)
    assigned_staff_id: int
    staffing_status: str = Field(required=True)
    position_created_at: datetime = Field(required=True)
    position_updated_at: datetime = Field(required=True)
    position_duration_hours: float = Field(default=1)
    staff_position_email: str = Field(required=False)

class Event(AbstractPayload):
    """
    Event Model.
    """
    event_id: int = Field(primary_key=True, required=True)
    client_id: int
    name: str = Field(required=True)
    start_timestamp: datetime = Field(required=True)
    end_timestamp: datetime = Field(required=True)
    created_at: datetime = Field(required=True)
    updated_at: datetime = Field(required=True)
    duration_hours: float = Field(default=1.0)
    formid: int = Field(required=True, alias='form_id')
    description: str
    status: str = Field(required=True)
    type: str = Field(required=True)
    program_id: int = Field(required=True)
    program_name: str = Field(required=True)
    store_id: int = Field(required=True)  # "store_id": 5432
    category: str = Field(required=False)
    event_positions: List[EventPosition] = Field(required=False)
    is_deleted: bool = Field(default=False)
    is_archived: bool = Field(default=False)
    ad_hoc: bool = Field(default=False)
    accounting_code: Optional[str] = Field(default=None)

    class Meta:
        strict = True
        as_objects = True
        name = 'events'
        schema: str = 'networkninja'


class EventPunch(AbstractPayload):
    """
    Event Punch Model.

    Example:
        {

                "cico_id": 4089,
                "event_id": 12272,
                "visitor_id": 18180,
                "latitude": "32.8066746",
                "longitude": "-97.426601",
                "cico_type": "out",
                "related_checkout_id": null,
                "total_hours": null,
                "client_id": 57,
                "orgid": 106,
                "visitor_name": "Margaret Ojeogwu",
                "timestamp_utc": "2025-03-22T01:17:36+00:00"
            }
    """
    cico_id: int = Field(primary_key=True, required=True)
    event_id: int = Field(required=True)
    visitor_id: int = Field(required=True)
    latitude: float
    longitude: float
    cico_type: str = Field(required=True)
    related_checkout_id: Optional[int]
    total_hours: float
    client_id: int = Field(required=True)
    orgid: int = Field(required=True)
    visitor_name: str = Field(required=False)
    event_timestamp: datetime = Field(required=True, alias='timestamp_utc')
    is_archived: bool = Field(default=False)
    is_deleted: bool = Field(default=False)
    visitor_email: str = Field(required=False)

    class Meta:
        strict = True
        as_objects = True
        name = 'evt_checkin_checkout'
        schema: str = 'networkninja'

    def __post_init__(self):
        super().__post_init__()
        if self.visitor_id:
            self.user_id = self.visitor_id
