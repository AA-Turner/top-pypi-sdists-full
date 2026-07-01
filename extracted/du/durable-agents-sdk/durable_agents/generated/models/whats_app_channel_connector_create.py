from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .whats_app_connector_secrets import WhatsAppConnectorSecrets

@dataclass
class WhatsAppChannelConnectorCreate(Parsable):
    # The name property
    name: Optional[str] = None
    # The provider property
    provider: Optional[str] = None
    # The whatsapp property
    whatsapp: Optional[WhatsAppConnectorSecrets] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> WhatsAppChannelConnectorCreate:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: WhatsAppChannelConnectorCreate
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return WhatsAppChannelConnectorCreate()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        from .whats_app_connector_secrets import WhatsAppConnectorSecrets

        from .whats_app_connector_secrets import WhatsAppConnectorSecrets

        fields: dict[str, Callable[[Any], None]] = {
            "name": lambda n : setattr(self, 'name', n.get_str_value()),
            "provider": lambda n : setattr(self, 'provider', n.get_str_value()),
            "whatsapp": lambda n : setattr(self, 'whatsapp', n.get_object_value(WhatsAppConnectorSecrets)),
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
        writer.write_object_value("whatsapp", self.whatsapp)
    

