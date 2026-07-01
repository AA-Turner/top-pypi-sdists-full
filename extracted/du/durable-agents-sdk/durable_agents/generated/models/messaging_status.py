from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .channel_endpoint import ChannelEndpoint
    from .messaging_status_provider import MessagingStatus_provider
    from .registered_phone import RegisteredPhone

@dataclass
class MessagingStatus(Parsable):
    # The endpoint property
    endpoint: Optional[ChannelEndpoint] = None
    # The provider property
    provider: Optional[MessagingStatus_provider] = None
    # The registered_phones property
    registered_phones: Optional[list[RegisteredPhone]] = None
    # The shared_number property
    shared_number: Optional[str] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> MessagingStatus:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: MessagingStatus
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return MessagingStatus()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        from .channel_endpoint import ChannelEndpoint
        from .messaging_status_provider import MessagingStatus_provider
        from .registered_phone import RegisteredPhone

        from .channel_endpoint import ChannelEndpoint
        from .messaging_status_provider import MessagingStatus_provider
        from .registered_phone import RegisteredPhone

        fields: dict[str, Callable[[Any], None]] = {
            "endpoint": lambda n : setattr(self, 'endpoint', n.get_object_value(ChannelEndpoint)),
            "provider": lambda n : setattr(self, 'provider', n.get_enum_value(MessagingStatus_provider)),
            "registered_phones": lambda n : setattr(self, 'registered_phones', n.get_collection_of_object_values(RegisteredPhone)),
            "shared_number": lambda n : setattr(self, 'shared_number', n.get_str_value()),
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
        writer.write_object_value("endpoint", self.endpoint)
        writer.write_enum_value("provider", self.provider)
        writer.write_collection_of_object_values("registered_phones", self.registered_phones)
        writer.write_str_value("shared_number", self.shared_number)
    

