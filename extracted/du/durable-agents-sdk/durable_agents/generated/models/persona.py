from __future__ import annotations
import datetime
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .entity_state import EntityState

@dataclass
class Persona(Parsable):
    # The created_at property
    created_at: Optional[datetime.datetime] = None
    # The id property
    id: Optional[str] = None
    # The instructions property
    instructions: Optional[str] = None
    # The name property
    name: Optional[str] = None
    # The role property
    role: Optional[str] = None
    # The state property
    state: Optional[EntityState] = None
    # The type property
    type: Optional[str] = None
    # The updated_at property
    updated_at: Optional[datetime.datetime] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> Persona:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: Persona
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return Persona()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        from .entity_state import EntityState

        from .entity_state import EntityState

        fields: dict[str, Callable[[Any], None]] = {
            "created_at": lambda n : setattr(self, 'created_at', n.get_datetime_value()),
            "id": lambda n : setattr(self, 'id', n.get_str_value()),
            "instructions": lambda n : setattr(self, 'instructions', n.get_str_value()),
            "name": lambda n : setattr(self, 'name', n.get_str_value()),
            "role": lambda n : setattr(self, 'role', n.get_str_value()),
            "state": lambda n : setattr(self, 'state', n.get_enum_value(EntityState)),
            "type": lambda n : setattr(self, 'type', n.get_str_value()),
            "updated_at": lambda n : setattr(self, 'updated_at', n.get_datetime_value()),
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
        writer.write_datetime_value("created_at", self.created_at)
        writer.write_str_value("id", self.id)
        writer.write_str_value("instructions", self.instructions)
        writer.write_str_value("name", self.name)
        writer.write_str_value("role", self.role)
        writer.write_enum_value("state", self.state)
        writer.write_str_value("type", self.type)
        writer.write_datetime_value("updated_at", self.updated_at)
    

