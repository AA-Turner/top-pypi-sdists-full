from __future__ import annotations
import datetime
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .audit_event_actor import AuditEvent_actor
    from .audit_event_data import AuditEvent_data
    from .ref import Ref

@dataclass
class AuditEvent(Parsable):
    # The actor property
    actor: Optional[AuditEvent_actor] = None
    # The created_at property
    created_at: Optional[datetime.datetime] = None
    # The data property
    data: Optional[AuditEvent_data] = None
    # The id property
    id: Optional[str] = None
    # The request_id property
    request_id: Optional[str] = None
    # The target property
    target: Optional[Ref] = None
    # The type property
    type: Optional[str] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> AuditEvent:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: AuditEvent
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return AuditEvent()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        from .audit_event_actor import AuditEvent_actor
        from .audit_event_data import AuditEvent_data
        from .ref import Ref

        from .audit_event_actor import AuditEvent_actor
        from .audit_event_data import AuditEvent_data
        from .ref import Ref

        fields: dict[str, Callable[[Any], None]] = {
            "actor": lambda n : setattr(self, 'actor', n.get_enum_value(AuditEvent_actor)),
            "created_at": lambda n : setattr(self, 'created_at', n.get_datetime_value()),
            "data": lambda n : setattr(self, 'data', n.get_object_value(AuditEvent_data)),
            "id": lambda n : setattr(self, 'id', n.get_str_value()),
            "request_id": lambda n : setattr(self, 'request_id', n.get_str_value()),
            "target": lambda n : setattr(self, 'target', n.get_object_value(Ref)),
            "type": lambda n : setattr(self, 'type', n.get_str_value()),
        }
        return fields
    
    def serialize(self,writer: SerializationWriter) -> None:
        """
        Serializes information the current object
        param writer: Serialization writer to use to serialize this model
        Returns: None
        """
        if writer is None:
            raise TypeError("writer cannot be null.")
        writer.write_enum_value("actor", self.actor)
        writer.write_datetime_value("created_at", self.created_at)
        writer.write_object_value("data", self.data)
        writer.write_str_value("id", self.id)
        writer.write_str_value("request_id", self.request_id)
        writer.write_object_value("target", self.target)
        writer.write_str_value("type", self.type)
    

