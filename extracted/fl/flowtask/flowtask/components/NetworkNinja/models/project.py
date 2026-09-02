from typing import Optional
from datetime import datetime
from datamodel import Field
from .abstract import AbstractPayload
from .organization import Organization
from .client import Client


class Project(AbstractPayload):
    """
    NN Projects related to a Client.

    Example payload:
    "payload": {
        "project_id": 595,
        "project_name": "Test Program",
        "is_active": true,
        "start_timestamp": "2025-02-01T00:00:00-06:00",
        "end_timestamp": "2025-02-28T00:00:00-06:00",
        "inserted_at": "2025-01-30T19:19:40-06:00",
        "updated_at": "2025-01-30T19:19:40-06:00",
        "description": "",
        "orgid": 69,
        "client_id": 56,
        "client_name": "EPSON"
    }
    """
    project_id: int = Field(primary_key=True, required=True)
    project_name: str
    is_active: bool = Field(default=True)
    start_timestamp: datetime
    end_timestamp: datetime
    inserted_at: datetime
    updated_at: datetime
    description: str
    orgid: Optional[Organization]
    client_id: Client
    client_name: str
    accounting_code: Optional[str] = Field(default=None)

    class Meta:
        strict = True
        as_objects = True
        name = 'projects'
        schema: str = 'networkninja'
