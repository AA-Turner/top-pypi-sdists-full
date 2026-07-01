from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .ref import Ref
    from .target_input_config import TargetInput_config
    from .target_input_type import TargetInput_type

@dataclass
class TargetInput(Parsable):
    # The authentication property
    authentication: Optional[Ref] = None
    # The config property
    config: Optional[TargetInput_config] = None
    # The default property
    default: Optional[bool] = None
    # The name property
    name: Optional[str] = None
    # The type property
    type: Optional[TargetInput_type] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> TargetInput:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: TargetInput
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return TargetInput()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        from .ref import Ref
        from .target_input_config import TargetInput_config
        from .target_input_type import TargetInput_type

        from .ref import Ref
        from .target_input_config import TargetInput_config
        from .target_input_type import TargetInput_type

        fields: dict[str, Callable[[Any], None]] = {
            "authentication": lambda n : setattr(self, 'authentication', n.get_object_value(Ref)),
            "config": lambda n : setattr(self, 'config', n.get_object_value(TargetInput_config)),
            "default": lambda n : setattr(self, 'default', n.get_bool_value()),
            "name": lambda n : setattr(self, 'name', n.get_str_value()),
            "type": lambda n : setattr(self, 'type', n.get_enum_value(TargetInput_type)),
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
        writer.write_object_value("authentication", self.authentication)
        writer.write_object_value("config", self.config)
        writer.write_bool_value("default", self.default)
        writer.write_str_value("name", self.name)
        writer.write_enum_value("type", self.type)
    

