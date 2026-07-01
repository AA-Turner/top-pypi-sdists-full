from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .channel_input_config import ChannelInput_config
    from .channel_status import ChannelStatus
    from .channel_type import ChannelType

@dataclass
class ChannelInput(Parsable):
    # The config property
    config: Optional[ChannelInput_config] = None
    # The status property
    status: Optional[ChannelStatus] = None
    # The type property
    type: Optional[ChannelType] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> ChannelInput:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: ChannelInput
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return ChannelInput()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        from .channel_input_config import ChannelInput_config
        from .channel_status import ChannelStatus
        from .channel_type import ChannelType

        from .channel_input_config import ChannelInput_config
        from .channel_status import ChannelStatus
        from .channel_type import ChannelType

        fields: dict[str, Callable[[Any], None]] = {
            "config": lambda n : setattr(self, 'config', n.get_object_value(ChannelInput_config)),
            "status": lambda n : setattr(self, 'status', n.get_enum_value(ChannelStatus)),
            "type": lambda n : setattr(self, 'type', n.get_enum_value(ChannelType)),
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
        writer.write_object_value("config", self.config)
        writer.write_enum_value("status", self.status)
        writer.write_enum_value("type", self.type)
    

