from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .telegram_connector_secrets import TelegramConnectorSecrets

@dataclass
class TelegramChannelConnectorCreate(Parsable):
    # The name property
    name: Optional[str] = None
    # The provider property
    provider: Optional[str] = None
    # The telegram property
    telegram: Optional[TelegramConnectorSecrets] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> TelegramChannelConnectorCreate:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: TelegramChannelConnectorCreate
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return TelegramChannelConnectorCreate()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        from .telegram_connector_secrets import TelegramConnectorSecrets

        from .telegram_connector_secrets import TelegramConnectorSecrets

        fields: dict[str, Callable[[Any], None]] = {
            "name": lambda n : setattr(self, 'name', n.get_str_value()),
            "provider": lambda n : setattr(self, 'provider', n.get_str_value()),
            "telegram": lambda n : setattr(self, 'telegram', n.get_object_value(TelegramConnectorSecrets)),
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
        writer.write_str_value("provider", self.provider)
        writer.write_object_value("telegram", self.telegram)
    

