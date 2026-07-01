from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .data_source_schedule import DataSourceSchedule

@dataclass
class DataSourceUpdate(Parsable):
    # The name property
    name: Optional[str] = None
    # The read_limit property
    read_limit: Optional[int] = None
    # The schedule property
    schedule: Optional[DataSourceSchedule] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> DataSourceUpdate:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: DataSourceUpdate
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return DataSourceUpdate()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        from .data_source_schedule import DataSourceSchedule

        from .data_source_schedule import DataSourceSchedule

        fields: dict[str, Callable[[Any], None]] = {
            "name": lambda n : setattr(self, 'name', n.get_str_value()),
            "read_limit": lambda n : setattr(self, 'read_limit', n.get_int_value()),
            "schedule": lambda n : setattr(self, 'schedule', n.get_enum_value(DataSourceSchedule)),
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
        writer.write_str_value("name", self.name)
        writer.write_int_value("read_limit", self.read_limit)
        writer.write_enum_value("schedule", self.schedule)
    

