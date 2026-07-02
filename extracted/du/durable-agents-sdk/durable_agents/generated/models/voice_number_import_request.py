from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

@dataclass
class VoiceNumberImportRequest(Parsable):
    # The label property
    label: Optional[str] = None
    # The phone property
    phone: Optional[str] = None
    # The provider_number_id property
    provider_number_id: Optional[str] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> VoiceNumberImportRequest:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: VoiceNumberImportRequest
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return VoiceNumberImportRequest()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        fields: dict[str, Callable[[Any], None]] = {
            "label": lambda n : setattr(self, 'label', n.get_str_value()),
            "phone": lambda n : setattr(self, 'phone', n.get_str_value()),
            "provider_number_id": lambda n : setattr(self, 'provider_number_id', n.get_str_value()),
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
        writer.write_str_value("label", self.label)
        writer.write_str_value("phone", self.phone)
        writer.write_str_value("provider_number_id", self.provider_number_id)
    

