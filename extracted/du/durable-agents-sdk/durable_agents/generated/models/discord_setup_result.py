from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import AdditionalDataHolder, Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .channel_connector import ChannelConnector
    from .discord_interactions_endpoint_registration import DiscordInteractionsEndpointRegistration
    from .discord_route_registry_result import DiscordRouteRegistryResult
    from .discord_setup_guide import DiscordSetupGuide
    from .discord_setup_result_missing_credentials import DiscordSetupResult_missing_credentials

from .discord_setup_guide import DiscordSetupGuide

@dataclass
class DiscordSetupResult(DiscordSetupGuide, AdditionalDataHolder, Parsable):
    # Stores additional data not described in the OpenAPI description found when deserializing. Can be used for serialization as well.
    additional_data: dict[str, Any] = field(default_factory=dict)

    # The connector property
    connector: Optional[ChannelConnector] = None
    # The created_connector property
    created_connector: Optional[bool] = None
    # The interactions_endpoint property
    interactions_endpoint: Optional[DiscordInteractionsEndpointRegistration] = None
    # The missing_credentials property
    missing_credentials: Optional[list[DiscordSetupResult_missing_credentials]] = None
    # The route_registry property
    route_registry: Optional[DiscordRouteRegistryResult] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> DiscordSetupResult:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: DiscordSetupResult
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return DiscordSetupResult()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        from .channel_connector import ChannelConnector
        from .discord_interactions_endpoint_registration import DiscordInteractionsEndpointRegistration
        from .discord_route_registry_result import DiscordRouteRegistryResult
        from .discord_setup_guide import DiscordSetupGuide
        from .discord_setup_result_missing_credentials import DiscordSetupResult_missing_credentials

        from .channel_connector import ChannelConnector
        from .discord_interactions_endpoint_registration import DiscordInteractionsEndpointRegistration
        from .discord_route_registry_result import DiscordRouteRegistryResult
        from .discord_setup_guide import DiscordSetupGuide
        from .discord_setup_result_missing_credentials import DiscordSetupResult_missing_credentials

        fields: dict[str, Callable[[Any], None]] = {
            "connector": lambda n : setattr(self, 'connector', n.get_object_value(ChannelConnector)),
            "created_connector": lambda n : setattr(self, 'created_connector', n.get_bool_value()),
            "interactions_endpoint": lambda n : setattr(self, 'interactions_endpoint', n.get_object_value(DiscordInteractionsEndpointRegistration)),
            "missing_credentials": lambda n : setattr(self, 'missing_credentials', n.get_collection_of_enum_values(DiscordSetupResult_missing_credentials)),
            "route_registry": lambda n : setattr(self, 'route_registry', n.get_object_value(DiscordRouteRegistryResult)),
        }
        super_fields = super().get_field_deserializers()
        fields.update(super_fields)
        return fields
    
    def serialize(self,writer: SerializationWriter) -> None:
        """
        Serializes information the current object
        param writer: Serialization writer to use to serialize this model
        Returns: None
        """
        if writer is None:
            raise TypeError("writer cannot be null.")
        super().serialize(writer)
        writer.write_object_value("connector", self.connector)
        writer.write_bool_value("created_connector", self.created_connector)
        writer.write_object_value("interactions_endpoint", self.interactions_endpoint)
        writer.write_collection_of_enum_values("missing_credentials", self.missing_credentials)
        writer.write_object_value("route_registry", self.route_registry)
        writer.write_additional_data_value(self.additional_data)
    

