from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .endpoint_provider import EndpointProvider
    from .endpoint_type import EndpointType

@dataclass
class ChannelBindingDelete(Parsable):
    # The channel property
    channel: Optional[str] = None
    # The conversation_id property
    conversation_id: Optional[str] = None
    # The email property
    email: Optional[str] = None
    # The endpoint property
    endpoint: Optional[str] = None
    # The provider property
    provider: Optional[EndpointProvider] = None
    # The team property
    team: Optional[str] = None
    # The tenant_id property
    tenant_id: Optional[str] = None
    # The type property
    type: Optional[EndpointType] = None
    # The workspace property
    workspace: Optional[str] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> ChannelBindingDelete:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: ChannelBindingDelete
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return ChannelBindingDelete()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        from .endpoint_provider import EndpointProvider
        from .endpoint_type import EndpointType

        from .endpoint_provider import EndpointProvider
        from .endpoint_type import EndpointType

        fields: dict[str, Callable[[Any], None]] = {
            "channel": lambda n : setattr(self, 'channel', n.get_str_value()),
            "conversation_id": lambda n : setattr(self, 'conversation_id', n.get_str_value()),
            "email": lambda n : setattr(self, 'email', n.get_str_value()),
            "endpoint": lambda n : setattr(self, 'endpoint', n.get_str_value()),
            "provider": lambda n : setattr(self, 'provider', n.get_enum_value(EndpointProvider)),
            "team": lambda n : setattr(self, 'team', n.get_str_value()),
            "tenant_id": lambda n : setattr(self, 'tenant_id', n.get_str_value()),
            "type": lambda n : setattr(self, 'type', n.get_enum_value(EndpointType)),
            "workspace": lambda n : setattr(self, 'workspace', n.get_str_value()),
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
        writer.write_str_value("channel", self.channel)
        writer.write_str_value("conversation_id", self.conversation_id)
        writer.write_str_value("email", self.email)
        writer.write_str_value("endpoint", self.endpoint)
        writer.write_enum_value("provider", self.provider)
        writer.write_str_value("team", self.team)
        writer.write_str_value("tenant_id", self.tenant_id)
        writer.write_enum_value("type", self.type)
        writer.write_str_value("workspace", self.workspace)
    

