from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .schedule_recurrence_type import Schedule_recurrence_type

@dataclass
class Schedule(Parsable):
    # The cron property
    cron: Optional[str] = None
    # The recurrence_type property
    recurrence_type: Optional[Schedule_recurrence_type] = None
    # The repeat_interval property
    repeat_interval: Optional[str] = None
    # The timezone property
    timezone: Optional[str] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> Schedule:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: Schedule
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return Schedule()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        from .schedule_recurrence_type import Schedule_recurrence_type

        from .schedule_recurrence_type import Schedule_recurrence_type

        fields: dict[str, Callable[[Any], None]] = {
            "cron": lambda n : setattr(self, 'cron', n.get_str_value()),
            "recurrence_type": lambda n : setattr(self, 'recurrence_type', n.get_enum_value(Schedule_recurrence_type)),
            "repeat_interval": lambda n : setattr(self, 'repeat_interval', n.get_str_value()),
            "timezone": lambda n : setattr(self, 'timezone', n.get_str_value()),
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
        writer.write_str_value("cron", self.cron)
        writer.write_enum_value("recurrence_type", self.recurrence_type)
        writer.write_str_value("repeat_interval", self.repeat_interval)
        writer.write_str_value("timezone", self.timezone)
    

