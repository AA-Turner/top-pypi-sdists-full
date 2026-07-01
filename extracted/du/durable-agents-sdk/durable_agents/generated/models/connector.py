from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .connector_auth_status import ConnectorAuthStatus
    from .connector_status import Connector_status
    from .connector_type import Connector_type

@dataclass
class Connector(Parsable):
    # The auth_status property
    auth_status: Optional[ConnectorAuthStatus] = None
    # The id property
    id: Optional[str] = None
    # The is_built_in property
    is_built_in: Optional[bool] = None
    # The is_enabled property
    is_enabled: Optional[bool] = None
    # The name property
    name: Optional[str] = None
    # The requires_oauth property
    requires_oauth: Optional[bool] = None
    # The resources_count property
    resources_count: Optional[int] = None
    # The status property
    status: Optional[Connector_status] = None
    # The tools_count property
    tools_count: Optional[int] = None
    # The type property
    type: Optional[Connector_type] = None
    # The url property
    url: Optional[str] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> Connector:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: Connector
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return Connector()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        from .connector_auth_status import ConnectorAuthStatus
        from .connector_status import Connector_status
        from .connector_type import Connector_type

        from .connector_auth_status import ConnectorAuthStatus
        from .connector_status import Connector_status
        from .connector_type import Connector_type

        fields: dict[str, Callable[[Any], None]] = {
            "auth_status": lambda n : setattr(self, 'auth_status', n.get_object_value(ConnectorAuthStatus)),
            "id": lambda n : setattr(self, 'id', n.get_str_value()),
            "is_built_in": lambda n : setattr(self, 'is_built_in', n.get_bool_value()),
            "is_enabled": lambda n : setattr(self, 'is_enabled', n.get_bool_value()),
            "name": lambda n : setattr(self, 'name', n.get_str_value()),
            "requires_oauth": lambda n : setattr(self, 'requires_oauth', n.get_bool_value()),
            "resources_count": lambda n : setattr(self, 'resources_count', n.get_int_value()),
            "status": lambda n : setattr(self, 'status', n.get_enum_value(Connector_status)),
            "tools_count": lambda n : setattr(self, 'tools_count', n.get_int_value()),
            "type": lambda n : setattr(self, 'type', n.get_enum_value(Connector_type)),
            "url": lambda n : setattr(self, 'url', n.get_str_value()),
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
        writer.write_object_value("auth_status", self.auth_status)
        writer.write_str_value("id", self.id)
        writer.write_bool_value("is_built_in", self.is_built_in)
        writer.write_bool_value("is_enabled", self.is_enabled)
        writer.write_str_value("name", self.name)
        writer.write_bool_value("requires_oauth", self.requires_oauth)
        writer.write_int_value("resources_count", self.resources_count)
        writer.write_enum_value("status", self.status)
        writer.write_int_value("tools_count", self.tools_count)
        writer.write_enum_value("type", self.type)
        writer.write_str_value("url", self.url)
    

