from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .channel_setup_guide_required_credentials import ChannelSetupGuide_required_credentials

@dataclass
class ChannelSetupGuide(Parsable):
    # The events_url property
    events_url: Optional[str] = None
    # The manifest_create_url property
    manifest_create_url: Optional[str] = None
    # The manifest_url property
    manifest_url: Optional[str] = None
    # The manifest_yaml property
    manifest_yaml: Optional[str] = None
    # The provider property
    provider: Optional[str] = None
    # The required_credentials property
    required_credentials: Optional[list[ChannelSetupGuide_required_credentials]] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> ChannelSetupGuide:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: ChannelSetupGuide
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return ChannelSetupGuide()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        from .channel_setup_guide_required_credentials import ChannelSetupGuide_required_credentials

        from .channel_setup_guide_required_credentials import ChannelSetupGuide_required_credentials

        fields: dict[str, Callable[[Any], None]] = {
            "events_url": lambda n : setattr(self, 'events_url', n.get_str_value()),
            "manifest_create_url": lambda n : setattr(self, 'manifest_create_url', n.get_str_value()),
            "manifest_url": lambda n : setattr(self, 'manifest_url', n.get_str_value()),
            "manifest_yaml": lambda n : setattr(self, 'manifest_yaml', n.get_str_value()),
            "provider": lambda n : setattr(self, 'provider', n.get_str_value()),
            "required_credentials": lambda n : setattr(self, 'required_credentials', n.get_collection_of_enum_values(ChannelSetupGuide_required_credentials)),
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
        writer.write_str_value("events_url", self.events_url)
        writer.write_str_value("manifest_create_url", self.manifest_create_url)
        writer.write_str_value("manifest_url", self.manifest_url)
        writer.write_str_value("manifest_yaml", self.manifest_yaml)
        writer.write_str_value("provider", self.provider)
        writer.write_collection_of_enum_values("required_credentials", self.required_credentials)
    

