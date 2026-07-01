from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .connector_update_env import ConnectorUpdate_env
    from .connector_update_headers import ConnectorUpdate_headers

@dataclass
class ConnectorUpdate(Parsable):
    # The env property
    env: Optional[ConnectorUpdate_env] = None
    # The headers property
    headers: Optional[ConnectorUpdate_headers] = None
    # The name property
    name: Optional[str] = None
    # The url property
    url: Optional[str] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> ConnectorUpdate:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: ConnectorUpdate
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return ConnectorUpdate()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        from .connector_update_env import ConnectorUpdate_env
        from .connector_update_headers import ConnectorUpdate_headers

        from .connector_update_env import ConnectorUpdate_env
        from .connector_update_headers import ConnectorUpdate_headers

        fields: dict[str, Callable[[Any], None]] = {
            "env": lambda n : setattr(self, 'env', n.get_object_value(ConnectorUpdate_env)),
            "headers": lambda n : setattr(self, 'headers', n.get_object_value(ConnectorUpdate_headers)),
            "name": lambda n : setattr(self, 'name', n.get_str_value()),
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
        writer.write_object_value("env", self.env)
        writer.write_object_value("headers", self.headers)
        writer.write_str_value("name", self.name)
        writer.write_str_value("url", self.url)
    

