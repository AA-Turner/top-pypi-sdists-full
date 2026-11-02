from ..base import Event
from ..event_types import EventType
from .chat_based_event import CustomerEventData
from ....utils.types.identifier import StrObjectId
from pydantic import Field, field_validator
from typing import Optional, ClassVar
from enum import StrEnum
from ....company.assets.contact_point import ContactPoint
from ....utils.types.serializer_type import SerializerType
import json


class ContactPointUpdateReason(StrEnum):
    """Por qué cambió este touchpoint.

    Hasta ahora un `contact_point.updated` era mudo: decía QUÉ quedó, nunca POR QUÉ.
    Con esto una reatribución manual, una fusión de fuentes y un movimiento automático
    de la capa inferida dejan de ser indistinguibles — que era la razón por la que la
    atribución inferida necesitaba un evento propio para anunciar el movimiento.

    Es opcional a propósito: los emisores que todavía no lo pasan siguen andando y
    quedan como `null`, que se lee «no lo sabemos», no «manual»."""
    INFERRED_SUGGESTED = "inferred_suggested"
    """Se congeló una sugerencia de anuncio sobre un chat orgánico."""
    INFERRED_RECEIPT = "inferred_receipt"
    """El recibo de Meta confirmó el origen publicitario y movió el touchpoint solo."""
    INFERRED_HUMAN = "inferred_human"
    """Una persona resolvió la sugerencia desde el panel."""
    MANUAL = "manual"
    """Alguien corrigió el origen a mano, sin sugerencia de por medio."""
    MERGE = "merge"
    """Una fusión de fuentes arrastró el touchpoint."""


class ContactPointData(CustomerEventData):
    contact_point_id: StrObjectId
    source_id: Optional[StrObjectId] = Field(default=None)
    new_chat : bool
    matched: bool
    wamid: Optional[str] = Field(default=None)
    time_from_request_to_match_seconds : Optional[int] = Field(default=None)
    topic_id : Optional[StrObjectId] = Field(default=None)
    contact_point: Optional[ContactPoint] = Field(default=None)
    update_reason: Optional[ContactPointUpdateReason] = Field(
        default=None,
        description="Por qué cambió el touchpoint. Null = emisor que todavía no lo informa.",
    )

    def model_dump_json(self, *args, **kwargs):
        dump = json.loads(super().model_dump_json(*args, **kwargs))
        dump['contact_point'] = self.contact_point.model_dump_json(serializer=SerializerType.API) if self.contact_point else None
        return dump

class ContactPointEvent(Event):
    """Event for contact point operations"""
    data: ContactPointData

    # Define valid event types for this event class
    VALID_TYPES: ClassVar[set] = {
        EventType.CONTACT_POINT_CREATED,
        EventType.CONTACT_POINT_UPDATED,
        EventType.CONTACT_POINT_DELETED
    }

    @field_validator('type')
    def validate_event_type(cls, value):
        """Ensure only valid contact point event types are used"""
        if value not in cls.VALID_TYPES:
            raise ValueError(f"Invalid event type for ContactPointEvent: {value}. "
                           f"Must be one of: {', '.join(str(t) for t in cls.VALID_TYPES)}")
        return value

    def model_dump_json(self, *args, **kwargs):
        dump = json.loads(super().model_dump_json(*args, **kwargs))
        dump['data'] = self.data.model_dump_json()
        return dump