from __future__ import annotations
import datetime
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .ref import Ref
    from .voice_number_provider import VoiceNumber_provider
    from .voice_number_status import VoiceNumber_status

@dataclass
class VoiceNumber(Parsable):
    # The agent property
    agent: Optional[Ref] = None
    # The created_at property
    created_at: Optional[datetime.datetime] = None
    # The label property
    label: Optional[str] = None
    # The phone_number property
    phone_number: Optional[str] = None
    # The provider property
    provider: Optional[VoiceNumber_provider] = None
    # The provider_number_id property
    provider_number_id: Optional[str] = None
    # The status property
    status: Optional[VoiceNumber_status] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> VoiceNumber:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: VoiceNumber
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return VoiceNumber()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        from .ref import Ref
        from .voice_number_provider import VoiceNumber_provider
        from .voice_number_status import VoiceNumber_status

        from .ref import Ref
        from .voice_number_provider import VoiceNumber_provider
        from .voice_number_status import VoiceNumber_status

        fields: dict[str, Callable[[Any], None]] = {
            "agent": lambda n : setattr(self, 'agent', n.get_object_value(Ref)),
            "created_at": lambda n : setattr(self, 'created_at', n.get_datetime_value()),
            "label": lambda n : setattr(self, 'label', n.get_str_value()),
            "phone_number": lambda n : setattr(self, 'phone_number', n.get_str_value()),
            "provider": lambda n : setattr(self, 'provider', n.get_enum_value(VoiceNumber_provider)),
            "provider_number_id": lambda n : setattr(self, 'provider_number_id', n.get_str_value()),
            "status": lambda n : setattr(self, 'status', n.get_enum_value(VoiceNumber_status)),
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
        writer.write_datetime_value("created_at", self.created_at)
        writer.write_str_value("label", self.label)
        writer.write_str_value("phone_number", self.phone_number)
        writer.write_enum_value("provider", self.provider)
        writer.write_str_value("provider_number_id", self.provider_number_id)
        writer.write_enum_value("status", self.status)
    

