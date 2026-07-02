from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .discord_setup_request_message_access import DiscordSetupRequest_message_access

@dataclass
class DiscordSetupRequest(Parsable):
    # The application_id property
    application_id: Optional[str] = None
    # The bot_token property
    bot_token: Optional[str] = None
    # The command property
    command: Optional[str] = None
    # The connector property
    connector: Optional[str] = None
    # The create_or_update_connector property
    create_or_update_connector: Optional[bool] = None
    # The guild_id property
    guild_id: Optional[str] = None
    # The message_access property
    message_access: Optional[DiscordSetupRequest_message_access] = None
    # The name property
    name: Optional[str] = None
    # The public_key property
    public_key: Optional[str] = None
    # The register_command property
    register_command: Optional[bool] = None
    # The register_interactions_endpoint property
    register_interactions_endpoint: Optional[bool] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> DiscordSetupRequest:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: DiscordSetupRequest
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return DiscordSetupRequest()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        from .discord_setup_request_message_access import DiscordSetupRequest_message_access

        from .discord_setup_request_message_access import DiscordSetupRequest_message_access

        fields: dict[str, Callable[[Any], None]] = {
            "application_id": lambda n : setattr(self, 'application_id', n.get_str_value()),
            "bot_token": lambda n : setattr(self, 'bot_token', n.get_str_value()),
            "command": lambda n : setattr(self, 'command', n.get_str_value()),
            "connector": lambda n : setattr(self, 'connector', n.get_str_value()),
            "create_or_update_connector": lambda n : setattr(self, 'create_or_update_connector', n.get_bool_value()),
            "guild_id": lambda n : setattr(self, 'guild_id', n.get_str_value()),
            "message_access": lambda n : setattr(self, 'message_access', n.get_enum_value(DiscordSetupRequest_message_access)),
            "name": lambda n : setattr(self, 'name', n.get_str_value()),
            "public_key": lambda n : setattr(self, 'public_key', n.get_str_value()),
            "register_command": lambda n : setattr(self, 'register_command', n.get_bool_value()),
            "register_interactions_endpoint": lambda n : setattr(self, 'register_interactions_endpoint', n.get_bool_value()),
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
        writer.write_str_value("application_id", self.application_id)
        writer.write_str_value("bot_token", self.bot_token)
        writer.write_str_value("command", self.command)
        writer.write_str_value("connector", self.connector)
        writer.write_bool_value("create_or_update_connector", self.create_or_update_connector)
        writer.write_str_value("guild_id", self.guild_id)
        writer.write_enum_value("message_access", self.message_access)
        writer.write_str_value("name", self.name)
        writer.write_str_value("public_key", self.public_key)
        writer.write_bool_value("register_command", self.register_command)
        writer.write_bool_value("register_interactions_endpoint", self.register_interactions_endpoint)
    

