from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .skill_argument import SkillArgument

@dataclass
class SkillCreate(Parsable):
    # The arguments property
    arguments: Optional[list[SkillArgument]] = None
    # The description property
    description: Optional[str] = None
    # The name property
    name: Optional[str] = None
    # The text property
    text: Optional[str] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> SkillCreate:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: SkillCreate
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return SkillCreate()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        from .skill_argument import SkillArgument

        from .skill_argument import SkillArgument

        fields: dict[str, Callable[[Any], None]] = {
            "arguments": lambda n : setattr(self, 'arguments', n.get_collection_of_object_values(SkillArgument)),
            "description": lambda n : setattr(self, 'description', n.get_str_value()),
            "name": lambda n : setattr(self, 'name', n.get_str_value()),
            "text": lambda n : setattr(self, 'text', n.get_str_value()),
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
        writer.write_str_value("description", self.description)
        writer.write_str_value("name", self.name)
        writer.write_str_value("text", self.text)
    

