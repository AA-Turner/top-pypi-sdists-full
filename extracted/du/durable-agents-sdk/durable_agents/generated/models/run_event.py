from __future__ import annotations
import datetime
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .run_event_data import RunEvent_data
    from .run_event_type import RunEventType

@dataclass
class RunEvent(Parsable):
    # The agent_id property
    agent_id: Optional[str] = None
    # The created_at property
    created_at: Optional[datetime.datetime] = None
    # Opaque cursor to resume after this event.
    cursor: Optional[str] = None
    # Type-specific event payload.
    data: Optional[RunEvent_data] = None
    # Deterministic public event identifier.
    id: Optional[str] = None
    # The run_id property
    run_id: Optional[str] = None
    # Monotonic public sequence within the run.
    sequence: Optional[int] = None
    # The type property
    type: Optional[RunEventType] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> RunEvent:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: RunEvent
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return RunEvent()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        from .run_event_data import RunEvent_data
        from .run_event_type import RunEventType

        from .run_event_data import RunEvent_data
        from .run_event_type import RunEventType

        fields: dict[str, Callable[[Any], None]] = {
            "agent_id": lambda n : setattr(self, 'agent_id', n.get_str_value()),
            "created_at": lambda n : setattr(self, 'created_at', n.get_datetime_value()),
            "cursor": lambda n : setattr(self, 'cursor', n.get_str_value()),
            "data": lambda n : setattr(self, 'data', n.get_object_value(RunEvent_data)),
            "id": lambda n : setattr(self, 'id', n.get_str_value()),
            "run_id": lambda n : setattr(self, 'run_id', n.get_str_value()),
            "sequence": lambda n : setattr(self, 'sequence', n.get_int_value()),
            "type": lambda n : setattr(self, 'type', n.get_enum_value(RunEventType)),
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
        writer.write_str_value("agent_id", self.agent_id)
        writer.write_datetime_value("created_at", self.created_at)
        writer.write_str_value("cursor", self.cursor)
        writer.write_object_value("data", self.data)
        writer.write_str_value("id", self.id)
        writer.write_str_value("run_id", self.run_id)
        writer.write_int_value("sequence", self.sequence)
        writer.write_enum_value("type", self.type)
    

