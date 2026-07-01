from __future__ import annotations
import datetime
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .entity_state import EntityState
    from .skill_argument import SkillArgument

@dataclass
class Skill(Parsable):
    # The arguments property
    arguments: Optional[list[SkillArgument]] = None
    # The created_at property
    created_at: Optional[datetime.datetime] = None
    # The description property
    description: Optional[str] = None
    # The id property
    id: Optional[str] = None
    # The name property
    name: Optional[str] = None
    # The state property
    state: Optional[EntityState] = None
    # The text property
    text: Optional[str] = None
    # The updated_at property
    updated_at: Optional[datetime.datetime] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> Skill:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: Skill
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return Skill()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        from .entity_state import EntityState
        from .skill_argument import SkillArgument

        from .entity_state import EntityState
        from .skill_argument import SkillArgument

        fields: dict[str, Callable[[Any], None]] = {
            "arguments": lambda n : setattr(self, 'arguments', n.get_collection_of_object_values(SkillArgument)),
            "created_at": lambda n : setattr(self, 'created_at', n.get_datetime_value()),
            "description": lambda n : setattr(self, 'description', n.get_str_value()),
            "id": lambda n : setattr(self, 'id', n.get_str_value()),
            "name": lambda n : setattr(self, 'name', n.get_str_value()),
            "state": lambda n : setattr(self, 'state', n.get_enum_value(EntityState)),
            "text": lambda n : setattr(self, 'text', n.get_str_value()),
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
        writer.write_collection_of_object_values("arguments", self.arguments)
        writer.write_datetime_value("created_at", self.created_at)
        writer.write_str_value("description", self.description)
        writer.write_str_value("id", self.id)
        writer.write_str_value("name", self.name)
        writer.write_enum_value("state", self.state)
        writer.write_str_value("text", self.text)
        writer.write_datetime_value("updated_at", self.updated_at)
    

