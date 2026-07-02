from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

@dataclass
class VoiceNumberCandidate(Parsable):
    # The display_name property
    display_name: Optional[str] = None
    # The locality property
    locality: Optional[str] = None
    # The phone_number property
    phone_number: Optional[str] = None
    # The region property
    region: Optional[str] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> VoiceNumberCandidate:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: VoiceNumberCandidate
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return VoiceNumberCandidate()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        fields: dict[str, Callable[[Any], None]] = {
            "display_name": lambda n : setattr(self, 'display_name', n.get_str_value()),
            "locality": lambda n : setattr(self, 'locality', n.get_str_value()),
            "phone_number": lambda n : setattr(self, 'phone_number', n.get_str_value()),
            "region": lambda n : setattr(self, 'region', n.get_str_value()),
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
        writer.write_str_value("display_name", self.display_name)
        writer.write_str_value("locality", self.locality)
        writer.write_str_value("phone_number", self.phone_number)
        writer.write_str_value("region", self.region)
    

