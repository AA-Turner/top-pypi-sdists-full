from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .channel_connector import ChannelConnector
    from .channel_endpoint import ChannelEndpoint
    from .channel_message_access import ChannelMessageAccess
    from .whats_app_route_registry_result import WhatsAppRouteRegistryResult
    from .whats_app_setup_result_missing_credentials import WhatsAppSetupResult_missing_credentials
    from .whats_app_setup_result_recommended_credentials import WhatsAppSetupResult_recommended_credentials
    from .whats_app_setup_result_required_credentials import WhatsAppSetupResult_required_credentials
    from .whats_app_setup_result_webhook_fields import WhatsAppSetupResult_webhook_fields

@dataclass
class WhatsAppSetupResult(Parsable):
    # The callback_url property
    callback_url: Optional[str] = None
    # The connector property
    connector: Optional[ChannelConnector] = None
    # The created_connector property
    created_connector: Optional[bool] = None
    # The effective_message_access property
    effective_message_access: Optional[ChannelMessageAccess] = None
    # The endpoint property
    endpoint: Optional[ChannelEndpoint] = None
    # The endpoint_identifier property
    endpoint_identifier: Optional[str] = None
    # The message_access property
    message_access: Optional[ChannelMessageAccess] = None
    # The message_access_capabilities property
    message_access_capabilities: Optional[list[ChannelMessageAccess]] = None
    # The missing_credentials property
    missing_credentials: Optional[list[WhatsAppSetupResult_missing_credentials]] = None
    # The permission_notes property
    permission_notes: Optional[list[str]] = None
    # The preflight_questions property
    preflight_questions: Optional[list[str]] = None
    # The provider property
    provider: Optional[str] = None
    # The recommended_credentials property
    recommended_credentials: Optional[list[WhatsAppSetupResult_recommended_credentials]] = None
    # The required_credentials property
    required_credentials: Optional[list[WhatsAppSetupResult_required_credentials]] = None
    # The route_registry property
    route_registry: Optional[WhatsAppRouteRegistryResult] = None
    # The steps property
    steps: Optional[list[str]] = None
    # The verify_token property
    verify_token: Optional[str] = None
    # The webhook_fields property
    webhook_fields: Optional[list[WhatsAppSetupResult_webhook_fields]] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> WhatsAppSetupResult:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: WhatsAppSetupResult
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return WhatsAppSetupResult()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        from .channel_connector import ChannelConnector
        from .channel_endpoint import ChannelEndpoint
        from .channel_message_access import ChannelMessageAccess
        from .whats_app_route_registry_result import WhatsAppRouteRegistryResult
        from .whats_app_setup_result_missing_credentials import WhatsAppSetupResult_missing_credentials
        from .whats_app_setup_result_recommended_credentials import WhatsAppSetupResult_recommended_credentials
        from .whats_app_setup_result_required_credentials import WhatsAppSetupResult_required_credentials
        from .whats_app_setup_result_webhook_fields import WhatsAppSetupResult_webhook_fields

        from .channel_connector import ChannelConnector
        from .channel_endpoint import ChannelEndpoint
        from .channel_message_access import ChannelMessageAccess
        from .whats_app_route_registry_result import WhatsAppRouteRegistryResult
        from .whats_app_setup_result_missing_credentials import WhatsAppSetupResult_missing_credentials
        from .whats_app_setup_result_recommended_credentials import WhatsAppSetupResult_recommended_credentials
        from .whats_app_setup_result_required_credentials import WhatsAppSetupResult_required_credentials
        from .whats_app_setup_result_webhook_fields import WhatsAppSetupResult_webhook_fields

        fields: dict[str, Callable[[Any], None]] = {
            "callback_url": lambda n : setattr(self, 'callback_url', n.get_str_value()),
            "connector": lambda n : setattr(self, 'connector', n.get_object_value(ChannelConnector)),
            "created_connector": lambda n : setattr(self, 'created_connector', n.get_bool_value()),
            "effective_message_access": lambda n : setattr(self, 'effective_message_access', n.get_enum_value(ChannelMessageAccess)),
            "endpoint": lambda n : setattr(self, 'endpoint', n.get_object_value(ChannelEndpoint)),
            "endpoint_identifier": lambda n : setattr(self, 'endpoint_identifier', n.get_str_value()),
            "message_access": lambda n : setattr(self, 'message_access', n.get_enum_value(ChannelMessageAccess)),
            "message_access_capabilities": lambda n : setattr(self, 'message_access_capabilities', n.get_collection_of_enum_values(ChannelMessageAccess)),
            "missing_credentials": lambda n : setattr(self, 'missing_credentials', n.get_collection_of_enum_values(WhatsAppSetupResult_missing_credentials)),
            "permission_notes": lambda n : setattr(self, 'permission_notes', n.get_collection_of_primitive_values(str)),
            "preflight_questions": lambda n : setattr(self, 'preflight_questions', n.get_collection_of_primitive_values(str)),
            "provider": lambda n : setattr(self, 'provider', n.get_str_value()),
            "recommended_credentials": lambda n : setattr(self, 'recommended_credentials', n.get_collection_of_enum_values(WhatsAppSetupResult_recommended_credentials)),
            "required_credentials": lambda n : setattr(self, 'required_credentials', n.get_collection_of_enum_values(WhatsAppSetupResult_required_credentials)),
            "route_registry": lambda n : setattr(self, 'route_registry', n.get_object_value(WhatsAppRouteRegistryResult)),
            "steps": lambda n : setattr(self, 'steps', n.get_collection_of_primitive_values(str)),
            "verify_token": lambda n : setattr(self, 'verify_token', n.get_str_value()),
            "webhook_fields": lambda n : setattr(self, 'webhook_fields', n.get_collection_of_enum_values(WhatsAppSetupResult_webhook_fields)),
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
        writer.write_str_value("callback_url", self.callback_url)
        writer.write_object_value("connector", self.connector)
        writer.write_bool_value("created_connector", self.created_connector)
        writer.write_enum_value("effective_message_access", self.effective_message_access)
        writer.write_object_value("endpoint", self.endpoint)
        writer.write_str_value("endpoint_identifier", self.endpoint_identifier)
        writer.write_enum_value("message_access", self.message_access)
        writer.write_collection_of_enum_values("message_access_capabilities", self.message_access_capabilities)
        writer.write_collection_of_enum_values("missing_credentials", self.missing_credentials)
        writer.write_collection_of_primitive_values("permission_notes", self.permission_notes)
        writer.write_collection_of_primitive_values("preflight_questions", self.preflight_questions)
        writer.write_str_value("provider", self.provider)
        writer.write_collection_of_enum_values("recommended_credentials", self.recommended_credentials)
        writer.write_collection_of_enum_values("required_credentials", self.required_credentials)
        writer.write_object_value("route_registry", self.route_registry)
        writer.write_collection_of_primitive_values("steps", self.steps)
        writer.write_str_value("verify_token", self.verify_token)
        writer.write_collection_of_enum_values("webhook_fields", self.webhook_fields)
    

