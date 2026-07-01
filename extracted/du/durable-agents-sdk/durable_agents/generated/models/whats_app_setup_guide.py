from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .whats_app_setup_guide_recommended_credentials import WhatsAppSetupGuide_recommended_credentials
    from .whats_app_setup_guide_required_credentials import WhatsAppSetupGuide_required_credentials
    from .whats_app_setup_guide_webhook_fields import WhatsAppSetupGuide_webhook_fields

@dataclass
class WhatsAppSetupGuide(Parsable):
    # The callback_url property
    callback_url: Optional[str] = None
    # The endpoint_identifier property
    endpoint_identifier: Optional[str] = None
    # The preflight_questions property
    preflight_questions: Optional[list[str]] = None
    # The provider property
    provider: Optional[str] = None
    # The recommended_credentials property
    recommended_credentials: Optional[list[WhatsAppSetupGuide_recommended_credentials]] = None
    # The required_credentials property
    required_credentials: Optional[list[WhatsAppSetupGuide_required_credentials]] = None
    # The steps property
    steps: Optional[list[str]] = None
    # The verify_token property
    verify_token: Optional[str] = None
    # The webhook_fields property
    webhook_fields: Optional[list[WhatsAppSetupGuide_webhook_fields]] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> WhatsAppSetupGuide:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: WhatsAppSetupGuide
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return WhatsAppSetupGuide()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        from .whats_app_setup_guide_recommended_credentials import WhatsAppSetupGuide_recommended_credentials
        from .whats_app_setup_guide_required_credentials import WhatsAppSetupGuide_required_credentials
        from .whats_app_setup_guide_webhook_fields import WhatsAppSetupGuide_webhook_fields

        from .whats_app_setup_guide_recommended_credentials import WhatsAppSetupGuide_recommended_credentials
        from .whats_app_setup_guide_required_credentials import WhatsAppSetupGuide_required_credentials
        from .whats_app_setup_guide_webhook_fields import WhatsAppSetupGuide_webhook_fields

        fields: dict[str, Callable[[Any], None]] = {
            "callback_url": lambda n : setattr(self, 'callback_url', n.get_str_value()),
            "endpoint_identifier": lambda n : setattr(self, 'endpoint_identifier', n.get_str_value()),
            "preflight_questions": lambda n : setattr(self, 'preflight_questions', n.get_collection_of_primitive_values(str)),
            "provider": lambda n : setattr(self, 'provider', n.get_str_value()),
            "recommended_credentials": lambda n : setattr(self, 'recommended_credentials', n.get_collection_of_enum_values(WhatsAppSetupGuide_recommended_credentials)),
            "required_credentials": lambda n : setattr(self, 'required_credentials', n.get_collection_of_enum_values(WhatsAppSetupGuide_required_credentials)),
            "steps": lambda n : setattr(self, 'steps', n.get_collection_of_primitive_values(str)),
            "verify_token": lambda n : setattr(self, 'verify_token', n.get_str_value()),
            "webhook_fields": lambda n : setattr(self, 'webhook_fields', n.get_collection_of_enum_values(WhatsAppSetupGuide_webhook_fields)),
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
        writer.write_str_value("endpoint_identifier", self.endpoint_identifier)
        writer.write_collection_of_primitive_values("preflight_questions", self.preflight_questions)
        writer.write_str_value("provider", self.provider)
        writer.write_collection_of_enum_values("recommended_credentials", self.recommended_credentials)
        writer.write_collection_of_enum_values("required_credentials", self.required_credentials)
        writer.write_collection_of_primitive_values("steps", self.steps)
        writer.write_str_value("verify_token", self.verify_token)
        writer.write_collection_of_enum_values("webhook_fields", self.webhook_fields)
    

