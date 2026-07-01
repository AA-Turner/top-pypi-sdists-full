from __future__ import annotations
import datetime
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .endpoint_provider import EndpointProvider
    from .endpoint_type import EndpointType
    from .ref import Ref

@dataclass
class ChannelBinding(Parsable):
    # The agent property
    agent: Optional[Ref] = None
    # The connector property
    connector: Optional[Ref] = None
    # The created_at property
    created_at: Optional[datetime.datetime] = None
    # The display_name property
    display_name: Optional[str] = None
    # The identifier property
    identifier: Optional[str] = None
    # The instructions property
    instructions: Optional[str] = None
    # The provider property
    provider: Optional[EndpointProvider] = None
    # The type property
    type: Optional[EndpointType] = None
    # The updated_at property
    updated_at: Optional[datetime.datetime] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> ChannelBinding:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: ChannelBinding
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return ChannelBinding()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        from .endpoint_provider import EndpointProvider
        from .endpoint_type import EndpointType
        from .ref import Ref

        from .endpoint_provider import EndpointProvider
        from .endpoint_type import EndpointType
        from .ref import Ref

        fields: dict[str, Callable[[Any], None]] = {
            "agent": lambda n : setattr(self, 'agent', n.get_object_value(Ref)),
            "connector": lambda n : setattr(self, 'connector', n.get_object_value(Ref)),
            "created_at": lambda n : setattr(self, 'created_at', n.get_datetime_value()),
            "display_name": lambda n : setattr(self, 'display_name', n.get_str_value()),
            "identifier": lambda n : setattr(self, 'identifier', n.get_str_value()),
            "instructions": lambda n : setattr(self, 'instructions', n.get_str_value()),
            "provider": lambda n : setattr(self, 'provider', n.get_enum_value(EndpointProvider)),
            "type": lambda n : setattr(self, 'type', n.get_enum_value(EndpointType)),
            "updated_at": lambda n : setattr(self, 'updated_at', n.get_datetime_value()),
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
        writer.write_object_value("agent", self.agent)
        writer.write_object_value("connector", self.connector)
        writer.write_datetime_value("created_at", self.created_at)
        writer.write_str_value("display_name", self.display_name)
        writer.write_str_value("identifier", self.identifier)
        writer.write_str_value("instructions", self.instructions)
        writer.write_enum_value("provider", self.provider)
        writer.write_enum_value("type", self.type)
        writer.write_datetime_value("updated_at", self.updated_at)
    

