from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import ComposedTypeWrapper, Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .....models.discord_channel_connector_create import DiscordChannelConnectorCreate
    from .....models.google_chat_channel_connector_create import GoogleChatChannelConnectorCreate
    from .....models.slack_channel_connector_create import SlackChannelConnectorCreate
    from .....models.teams_channel_connector_create import TeamsChannelConnectorCreate
    from .....models.telegram_channel_connector_create import TelegramChannelConnectorCreate
    from .....models.whats_app_channel_connector_create import WhatsAppChannelConnectorCreate

@dataclass
class ChannelConnectorCreate(ComposedTypeWrapper, Parsable):
    """
    Composed type wrapper for classes DiscordChannelConnectorCreate, GoogleChatChannelConnectorCreate, SlackChannelConnectorCreate, TeamsChannelConnectorCreate, TelegramChannelConnectorCreate, WhatsAppChannelConnectorCreate
    """
    # Composed type representation for type DiscordChannelConnectorCreate
    discord_channel_connector_create: Optional[DiscordChannelConnectorCreate] = None
    # Composed type representation for type GoogleChatChannelConnectorCreate
    google_chat_channel_connector_create: Optional[GoogleChatChannelConnectorCreate] = None
    # Composed type representation for type SlackChannelConnectorCreate
    slack_channel_connector_create: Optional[SlackChannelConnectorCreate] = None
    # Composed type representation for type TeamsChannelConnectorCreate
    teams_channel_connector_create: Optional[TeamsChannelConnectorCreate] = None
    # Composed type representation for type TelegramChannelConnectorCreate
    telegram_channel_connector_create: Optional[TelegramChannelConnectorCreate] = None
    # Composed type representation for type WhatsAppChannelConnectorCreate
    whats_app_channel_connector_create: Optional[WhatsAppChannelConnectorCreate] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> ChannelConnectorCreate:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: ChannelConnectorCreate
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        try:
            child_node = parse_node.get_child_node("provider")
            mapping_value = child_node.get_str_value() if child_node else None
        except AttributeError:
            mapping_value = None
        result = ChannelConnectorCreate()
        if mapping_value and mapping_value.casefold() == "discord".casefold():
            from .....models.discord_channel_connector_create import DiscordChannelConnectorCreate

            result.discord_channel_connector_create = DiscordChannelConnectorCreate()
        elif mapping_value and mapping_value.casefold() == "google_chat".casefold():
            from .....models.google_chat_channel_connector_create import GoogleChatChannelConnectorCreate

            result.google_chat_channel_connector_create = GoogleChatChannelConnectorCreate()
        elif mapping_value and mapping_value.casefold() == "slack".casefold():
            from .....models.slack_channel_connector_create import SlackChannelConnectorCreate

            result.slack_channel_connector_create = SlackChannelConnectorCreate()
        elif mapping_value and mapping_value.casefold() == "teams".casefold():
            from .....models.teams_channel_connector_create import TeamsChannelConnectorCreate

            result.teams_channel_connector_create = TeamsChannelConnectorCreate()
        elif mapping_value and mapping_value.casefold() == "telegram".casefold():
            from .....models.telegram_channel_connector_create import TelegramChannelConnectorCreate

            result.telegram_channel_connector_create = TelegramChannelConnectorCreate()
        elif mapping_value and mapping_value.casefold() == "whatsapp".casefold():
            from .....models.whats_app_channel_connector_create import WhatsAppChannelConnectorCreate

            result.whats_app_channel_connector_create = WhatsAppChannelConnectorCreate()
        return result
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        from .....models.discord_channel_connector_create import DiscordChannelConnectorCreate
        from .....models.google_chat_channel_connector_create import GoogleChatChannelConnectorCreate
        from .....models.slack_channel_connector_create import SlackChannelConnectorCreate
        from .....models.teams_channel_connector_create import TeamsChannelConnectorCreate
        from .....models.telegram_channel_connector_create import TelegramChannelConnectorCreate
        from .....models.whats_app_channel_connector_create import WhatsAppChannelConnectorCreate

        if self.discord_channel_connector_create:
            return self.discord_channel_connector_create.get_field_deserializers()
        if self.google_chat_channel_connector_create:
            return self.google_chat_channel_connector_create.get_field_deserializers()
        if self.slack_channel_connector_create:
            return self.slack_channel_connector_create.get_field_deserializers()
        if self.teams_channel_connector_create:
            return self.teams_channel_connector_create.get_field_deserializers()
        if self.telegram_channel_connector_create:
            return self.telegram_channel_connector_create.get_field_deserializers()
        if self.whats_app_channel_connector_create:
            return self.whats_app_channel_connector_create.get_field_deserializers()
        return {}
    
    def serialize(self,writer: SerializationWriter) -> None:
        """
        Serializes information the current object
        param writer: Serialization writer to use to serialize this model
        Returns: None
        """
        if writer is None:
            raise TypeError("writer cannot be null.")
        if self.discord_channel_connector_create:
            writer.write_object_value(None, self.discord_channel_connector_create)
        elif self.google_chat_channel_connector_create:
            writer.write_object_value(None, self.google_chat_channel_connector_create)
        elif self.slack_channel_connector_create:
            writer.write_object_value(None, self.slack_channel_connector_create)
        elif self.teams_channel_connector_create:
            writer.write_object_value(None, self.teams_channel_connector_create)
        elif self.telegram_channel_connector_create:
            writer.write_object_value(None, self.telegram_channel_connector_create)
        elif self.whats_app_channel_connector_create:
            writer.write_object_value(None, self.whats_app_channel_connector_create)
    

