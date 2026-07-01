from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

@dataclass
class SlackConnectorSecrets(Parsable):
    # The app_id property
    app_id: Optional[str] = None
    # The bot_token property
    bot_token: Optional[str] = None
    # The signing_secret property
    signing_secret: Optional[str] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> SlackConnectorSecrets:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: SlackConnectorSecrets
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return SlackConnectorSecrets()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        fields: dict[str, Callable[[Any], None]] = {
            "app_id": lambda n : setattr(self, 'app_id', n.get_str_value()),
            "bot_token": lambda n : setattr(self, 'bot_token', n.get_str_value()),
            "signing_secret": lambda n : setattr(self, 'signing_secret', n.get_str_value()),
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
        writer.write_str_value("app_id", self.app_id)
        writer.write_str_value("bot_token", self.bot_token)
        writer.write_str_value("signing_secret", self.signing_secret)
    

