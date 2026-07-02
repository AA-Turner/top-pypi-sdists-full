from __future__ import annotations
import datetime
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .channel_connector_status import ChannelConnector_status
    from .channel_message_access import ChannelMessageAccess
    from .connector_provider import ConnectorProvider

@dataclass
class ChannelConnector(Parsable):
    # The created_at property
    created_at: Optional[datetime.datetime] = None
    # The effective_message_access property
    effective_message_access: Optional[ChannelMessageAccess] = None
    # The id property
    id: Optional[str] = None
    # The message_access property
    message_access: Optional[ChannelMessageAccess] = None
    # The name property
    name: Optional[str] = None
    # The provider property
    provider: Optional[ConnectorProvider] = None
    # The status property
    status: Optional[ChannelConnector_status] = None
    # The updated_at property
    updated_at: Optional[datetime.datetime] = None
    # The workspace_identifier property
    workspace_identifier: Optional[str] = None
    # The workspace_name property
    workspace_name: Optional[str] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> ChannelConnector:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: ChannelConnector
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return ChannelConnector()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        from .channel_connector_status import ChannelConnector_status
        from .channel_message_access import ChannelMessageAccess
        from .connector_provider import ConnectorProvider

        from .channel_connector_status import ChannelConnector_status
        from .channel_message_access import ChannelMessageAccess
        from .connector_provider import ConnectorProvider

        fields: dict[str, Callable[[Any], None]] = {
            "created_at": lambda n : setattr(self, 'created_at', n.get_datetime_value()),
            "effective_message_access": lambda n : setattr(self, 'effective_message_access', n.get_enum_value(ChannelMessageAccess)),
            "id": lambda n : setattr(self, 'id', n.get_str_value()),
            "message_access": lambda n : setattr(self, 'message_access', n.get_enum_value(ChannelMessageAccess)),
            "name": lambda n : setattr(self, 'name', n.get_str_value()),
            "provider": lambda n : setattr(self, 'provider', n.get_enum_value(ConnectorProvider)),
            "status": lambda n : setattr(self, 'status', n.get_enum_value(ChannelConnector_status)),
            "updated_at": lambda n : setattr(self, 'updated_at', n.get_datetime_value()),
            "workspace_identifier": lambda n : setattr(self, 'workspace_identifier', n.get_str_value()),
            "workspace_name": lambda n : setattr(self, 'workspace_name', n.get_str_value()),
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
        writer.write_datetime_value("created_at", self.created_at)
        writer.write_enum_value("effective_message_access", self.effective_message_access)
        writer.write_str_value("id", self.id)
        writer.write_enum_value("message_access", self.message_access)
        writer.write_str_value("name", self.name)
        writer.write_enum_value("provider", self.provider)
        writer.write_enum_value("status", self.status)
        writer.write_datetime_value("updated_at", self.updated_at)
        writer.write_str_value("workspace_identifier", self.workspace_identifier)
        writer.write_str_value("workspace_name", self.workspace_name)
    

