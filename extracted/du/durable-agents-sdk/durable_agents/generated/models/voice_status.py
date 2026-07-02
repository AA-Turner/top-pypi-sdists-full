from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .voice_number import VoiceNumber
    from .voice_status_provider import VoiceStatus_provider

@dataclass
class VoiceStatus(Parsable):
    # The bridge_configured property
    bridge_configured: Optional[bool] = None
    # The endpoint_count property
    endpoint_count: Optional[int] = None
    # The numbers property
    numbers: Optional[list[VoiceNumber]] = None
    # The provider property
    provider: Optional[VoiceStatus_provider] = None
    # The twilio_configured property
    twilio_configured: Optional[bool] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> VoiceStatus:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: VoiceStatus
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return VoiceStatus()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        from .voice_number import VoiceNumber
        from .voice_status_provider import VoiceStatus_provider

        from .voice_number import VoiceNumber
        from .voice_status_provider import VoiceStatus_provider

        fields: dict[str, Callable[[Any], None]] = {
            "bridge_configured": lambda n : setattr(self, 'bridge_configured', n.get_bool_value()),
            "endpoint_count": lambda n : setattr(self, 'endpoint_count', n.get_int_value()),
            "numbers": lambda n : setattr(self, 'numbers', n.get_collection_of_object_values(VoiceNumber)),
            "provider": lambda n : setattr(self, 'provider', n.get_enum_value(VoiceStatus_provider)),
            "twilio_configured": lambda n : setattr(self, 'twilio_configured', n.get_bool_value()),
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
        writer.write_bool_value("bridge_configured", self.bridge_configured)
        writer.write_int_value("endpoint_count", self.endpoint_count)
        writer.write_collection_of_object_values("numbers", self.numbers)
        writer.write_enum_value("provider", self.provider)
        writer.write_bool_value("twilio_configured", self.twilio_configured)
    

