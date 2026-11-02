from ..base import Event
from ..event_types import EventType
from .chat_based_event import CustomerEventData
from ....chat.quality_scoring import QualityScore
from pydantic import Field
from typing import ClassVar
from ....utils.types.identifier import StrObjectId
import json

class QualityScoringData(CustomerEventData):
    time_to_score_seconds: int = Field(description="The time it took the chat to get the score since the chat creation")
    quality_score: QualityScore

class QualityScoringEvent(Event):
    """Used for client related events, such as a new chat, a touchpoint, etc."""
    data: QualityScoringData

    VALID_TYPES: ClassVar[set] = {
        EventType.GOOD_QUALITY_SCORE_ASSIGNED,
        EventType.BAD_QUALITY_SCORE_ASSIGNED,
        EventType.NEUTRAL_QUALITY_SCORE_ASSIGNED
    }

    def model_dump_json(self, *args, **kwargs):
        dump = json.loads(super().model_dump_json(*args, **kwargs))
        dump['data'] = self.data.model_dump_json()
        return dump