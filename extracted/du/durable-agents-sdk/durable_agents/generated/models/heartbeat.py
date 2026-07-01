from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .heartbeat_probe_thresholds import Heartbeat_probe_thresholds

@dataclass
class Heartbeat(Parsable):
    # The active_days property
    active_days: Optional[list[int]] = None
    # The active_hours_end property
    active_hours_end: Optional[str] = None
    # The active_hours_start property
    active_hours_start: Optional[str] = None
    # The enabled property
    enabled: Optional[bool] = None
    # The frequency_minutes property
    frequency_minutes: Optional[int] = None
    # The off_hours_frequency_minutes property
    off_hours_frequency_minutes: Optional[int] = None
    # The probe_thresholds property
    probe_thresholds: Optional[Heartbeat_probe_thresholds] = None
    # The timezone property
    timezone: Optional[str] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> Heartbeat:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: Heartbeat
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return Heartbeat()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        from .heartbeat_probe_thresholds import Heartbeat_probe_thresholds

        from .heartbeat_probe_thresholds import Heartbeat_probe_thresholds

        fields: dict[str, Callable[[Any], None]] = {
            "active_days": lambda n : setattr(self, 'active_days', n.get_collection_of_primitive_values(int)),
            "active_hours_end": lambda n : setattr(self, 'active_hours_end', n.get_str_value()),
            "active_hours_start": lambda n : setattr(self, 'active_hours_start', n.get_str_value()),
            "enabled": lambda n : setattr(self, 'enabled', n.get_bool_value()),
            "frequency_minutes": lambda n : setattr(self, 'frequency_minutes', n.get_int_value()),
            "off_hours_frequency_minutes": lambda n : setattr(self, 'off_hours_frequency_minutes', n.get_int_value()),
            "probe_thresholds": lambda n : setattr(self, 'probe_thresholds', n.get_object_value(Heartbeat_probe_thresholds)),
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
        writer.write_collection_of_primitive_values("active_days", self.active_days)
        writer.write_str_value("active_hours_end", self.active_hours_end)
        writer.write_str_value("active_hours_start", self.active_hours_start)
        writer.write_bool_value("enabled", self.enabled)
        writer.write_int_value("frequency_minutes", self.frequency_minutes)
        writer.write_int_value("off_hours_frequency_minutes", self.off_hours_frequency_minutes)
        writer.write_object_value("probe_thresholds", self.probe_thresholds)
        writer.write_str_value("timezone", self.timezone)
    

