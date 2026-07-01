from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

@dataclass
class WhatsAppSetupRequest(Parsable):
    # The access_token property
    access_token: Optional[str] = None
    # The app_secret property
    app_secret: Optional[str] = None
    # The connector property
    connector: Optional[str] = None
    # The create_or_update_connector property
    create_or_update_connector: Optional[bool] = None
    # The name property
    name: Optional[str] = None
    # The phone_number_id property
    phone_number_id: Optional[str] = None
    # The sync_route_registry property
    sync_route_registry: Optional[bool] = None
    # The verify_token property
    verify_token: Optional[str] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> WhatsAppSetupRequest:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: WhatsAppSetupRequest
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return WhatsAppSetupRequest()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        fields: dict[str, Callable[[Any], None]] = {
            "access_token": lambda n : setattr(self, 'access_token', n.get_str_value()),
            "app_secret": lambda n : setattr(self, 'app_secret', n.get_str_value()),
            "connector": lambda n : setattr(self, 'connector', n.get_str_value()),
            "create_or_update_connector": lambda n : setattr(self, 'create_or_update_connector', n.get_bool_value()),
            "name": lambda n : setattr(self, 'name', n.get_str_value()),
            "phone_number_id": lambda n : setattr(self, 'phone_number_id', n.get_str_value()),
            "sync_route_registry": lambda n : setattr(self, 'sync_route_registry', n.get_bool_value()),
            "verify_token": lambda n : setattr(self, 'verify_token', n.get_str_value()),
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
        writer.write_str_value("access_token", self.access_token)
        writer.write_str_value("app_secret", self.app_secret)
        writer.write_str_value("connector", self.connector)
        writer.write_bool_value("create_or_update_connector", self.create_or_update_connector)
        writer.write_str_value("name", self.name)
        writer.write_str_value("phone_number_id", self.phone_number_id)
        writer.write_bool_value("sync_route_registry", self.sync_route_registry)
        writer.write_str_value("verify_token", self.verify_token)
    

