from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .discord_command_registration_scope import DiscordCommandRegistration_scope

@dataclass
class DiscordCommandRegistration(Parsable):
    # The guild_id property
    guild_id: Optional[str] = None
    # The name property
    name: Optional[str] = None
    # The option property
    option: Optional[str] = None
    # The registered property
    registered: Optional[bool] = None
    # The scope property
    scope: Optional[DiscordCommandRegistration_scope] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> DiscordCommandRegistration:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: DiscordCommandRegistration
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return DiscordCommandRegistration()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        from .discord_command_registration_scope import DiscordCommandRegistration_scope

        from .discord_command_registration_scope import DiscordCommandRegistration_scope

        fields: dict[str, Callable[[Any], None]] = {
            "guild_id": lambda n : setattr(self, 'guild_id', n.get_str_value()),
            "name": lambda n : setattr(self, 'name', n.get_str_value()),
            "option": lambda n : setattr(self, 'option', n.get_str_value()),
            "registered": lambda n : setattr(self, 'registered', n.get_bool_value()),
            "scope": lambda n : setattr(self, 'scope', n.get_enum_value(DiscordCommandRegistration_scope)),
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
        writer.write_str_value("guild_id", self.guild_id)
        writer.write_str_value("name", self.name)
        writer.write_str_value("option", self.option)
        writer.write_bool_value("registered", self.registered)
        writer.write_enum_value("scope", self.scope)
    

