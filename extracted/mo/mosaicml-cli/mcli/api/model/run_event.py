""" Defines a Run Event """
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict

from mcli.api.schema.generic_model import DeserializableModel, convert_datetime
from mcli.utils.utils_event_type import EventType


@dataclass()
class FormattedRunEvent(DeserializableModel):
    """ Formatted Run Event """

    event_type: EventType | str
    event_time: datetime
    event_message: str
    resumption_index: int = 0

    @classmethod
    def from_mapi_response(cls, response: Dict[str, Any]) -> FormattedRunEvent:
        """Load the formatted run event from MAPI response.
        """

        args = {
            'resumption_index': response['resumptionIndex'],
            'event_type': resolve_event_type(response['eventType']),
            'event_time': convert_datetime(response['eventTime']),
            'event_message': response['eventMessage'],
        }
        return cls(**args)


@dataclass()
class RunEvent(DeserializableModel):
    """ Run Event """
    id: str
    run_id: str
    execution_id: str
    event_type: EventType | str
    event_data: Dict[str, Any]
    updated_at: datetime

    @classmethod
    def from_mapi_response(cls, response: Dict[str, Any]) -> RunEvent:
        """Load the run event from MAPI response.
        """
        args = {
            'id': response['id'],
            'run_id': response['runId'],
            'execution_id': response['executionId'],
            'event_type': resolve_event_type(response['eventType']),
            'event_data': response['eventData'],
            'updated_at': convert_datetime(response['updatedAt']),
        }
        return cls(**args)


def resolve_event_type(response: str) -> EventType | str:
    try:
        event_type = EventType(response)
    except ValueError:
        event_type = response
    return event_type
