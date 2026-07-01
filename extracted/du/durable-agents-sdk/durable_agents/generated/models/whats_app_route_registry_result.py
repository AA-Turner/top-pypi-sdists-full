from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

@dataclass
class WhatsAppRouteRegistryResult(Parsable):
    # The phone_number_id_synced property
    phone_number_id_synced: Optional[bool] = None
    # The verify_token_synced property
    verify_token_synced: Optional[bool] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> WhatsAppRouteRegistryResult:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: WhatsAppRouteRegistryResult
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return WhatsAppRouteRegistryResult()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        fields: dict[str, Callable[[Any], None]] = {
            "phone_number_id_synced": lambda n : setattr(self, 'phone_number_id_synced', n.get_bool_value()),
            "verify_token_synced": lambda n : setattr(self, 'verify_token_synced', n.get_bool_value()),
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
        writer.write_bool_value("phone_number_id_synced", self.phone_number_id_synced)
        writer.write_bool_value("verify_token_synced", self.verify_token_synced)
    

