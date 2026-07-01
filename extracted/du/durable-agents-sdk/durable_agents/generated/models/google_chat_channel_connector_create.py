from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .google_chat_connector_secrets import GoogleChatConnectorSecrets

@dataclass
class GoogleChatChannelConnectorCreate(Parsable):
    # The google_chat property
    google_chat: Optional[GoogleChatConnectorSecrets] = None
    # The name property
    name: Optional[str] = None
    # The provider property
    provider: Optional[str] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> GoogleChatChannelConnectorCreate:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: GoogleChatChannelConnectorCreate
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return GoogleChatChannelConnectorCreate()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        from .google_chat_connector_secrets import GoogleChatConnectorSecrets

        from .google_chat_connector_secrets import GoogleChatConnectorSecrets

        fields: dict[str, Callable[[Any], None]] = {
            "google_chat": lambda n : setattr(self, 'google_chat', n.get_object_value(GoogleChatConnectorSecrets)),
            "name": lambda n : setattr(self, 'name', n.get_str_value()),
            "provider": lambda n : setattr(self, 'provider', n.get_str_value()),
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
        writer.write_object_value("google_chat", self.google_chat)
        writer.write_str_value("name", self.name)
        writer.write_str_value("provider", self.provider)
    

