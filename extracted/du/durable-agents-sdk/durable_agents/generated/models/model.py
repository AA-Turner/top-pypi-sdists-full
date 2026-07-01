from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .model_durable_preset import Model_durable_preset

@dataclass
class Model(Parsable):
    # The capabilities property
    capabilities: Optional[list[str]] = None
    # The display_name property
    display_name: Optional[str] = None
    # The durable_preset property
    durable_preset: Optional[Model_durable_preset] = None
    # The id property
    id: Optional[str] = None
    # The name property
    name: Optional[str] = None
    # The provider property
    provider: Optional[str] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> Model:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: Model
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return Model()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        from .model_durable_preset import Model_durable_preset

        from .model_durable_preset import Model_durable_preset

        fields: dict[str, Callable[[Any], None]] = {
            "capabilities": lambda n : setattr(self, 'capabilities', n.get_collection_of_primitive_values(str)),
            "display_name": lambda n : setattr(self, 'display_name', n.get_str_value()),
            "durable_preset": lambda n : setattr(self, 'durable_preset', n.get_object_value(Model_durable_preset)),
            "id": lambda n : setattr(self, 'id', n.get_str_value()),
            "name": lambda n : setattr(self, 'name', n.get_str_value()),
            "provider": lambda n : setattr(self, 'provider', n.get_str_value()),
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
        writer.write_collection_of_primitive_values("capabilities", self.capabilities)
        writer.write_str_value("display_name", self.display_name)
        writer.write_object_value("durable_preset", self.durable_preset)
        writer.write_str_value("id", self.id)
        writer.write_str_value("name", self.name)
        writer.write_str_value("provider", self.provider)
    

