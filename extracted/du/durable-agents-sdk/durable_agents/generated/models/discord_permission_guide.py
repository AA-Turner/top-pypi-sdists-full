from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .discord_permission_guide_names import DiscordPermissionGuide_names

@dataclass
class DiscordPermissionGuide(Parsable):
    # The integer property
    integer: Optional[str] = None
    # The names property
    names: Optional[list[DiscordPermissionGuide_names]] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> DiscordPermissionGuide:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: DiscordPermissionGuide
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return DiscordPermissionGuide()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        from .discord_permission_guide_names import DiscordPermissionGuide_names

        from .discord_permission_guide_names import DiscordPermissionGuide_names

        fields: dict[str, Callable[[Any], None]] = {
            "integer": lambda n : setattr(self, 'integer', n.get_str_value()),
            "names": lambda n : setattr(self, 'names', n.get_collection_of_enum_values(DiscordPermissionGuide_names)),
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
        writer.write_str_value("integer", self.integer)
        writer.write_collection_of_enum_values("names", self.names)
    

