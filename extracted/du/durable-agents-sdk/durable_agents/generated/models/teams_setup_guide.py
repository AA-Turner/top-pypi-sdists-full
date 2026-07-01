from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .teams_setup_guide_do_not_proceed_until import TeamsSetupGuide_do_not_proceed_until
    from .teams_setup_guide_recommended_bot_type import TeamsSetupGuide_recommended_bot_type
    from .teams_setup_guide_required_credentials import TeamsSetupGuide_required_credentials

@dataclass
class TeamsSetupGuide(Parsable):
    # The default_package_filename property
    default_package_filename: Optional[str] = None
    # The do_not_proceed_until property
    do_not_proceed_until: Optional[TeamsSetupGuide_do_not_proceed_until] = None
    # The manifest_url property
    manifest_url: Optional[str] = None
    # The messages_url property
    messages_url: Optional[str] = None
    # The preflight_questions property
    preflight_questions: Optional[list[str]] = None
    # The provider property
    provider: Optional[str] = None
    # The recommended_bot_type property
    recommended_bot_type: Optional[TeamsSetupGuide_recommended_bot_type] = None
    # The required_credentials property
    required_credentials: Optional[list[TeamsSetupGuide_required_credentials]] = None
    # The steps property
    steps: Optional[list[str]] = None
    # The token_scope property
    token_scope: Optional[str] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> TeamsSetupGuide:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: TeamsSetupGuide
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return TeamsSetupGuide()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        from .teams_setup_guide_do_not_proceed_until import TeamsSetupGuide_do_not_proceed_until
        from .teams_setup_guide_recommended_bot_type import TeamsSetupGuide_recommended_bot_type
        from .teams_setup_guide_required_credentials import TeamsSetupGuide_required_credentials

        from .teams_setup_guide_do_not_proceed_until import TeamsSetupGuide_do_not_proceed_until
        from .teams_setup_guide_recommended_bot_type import TeamsSetupGuide_recommended_bot_type
        from .teams_setup_guide_required_credentials import TeamsSetupGuide_required_credentials

        fields: dict[str, Callable[[Any], None]] = {
            "default_package_filename": lambda n : setattr(self, 'default_package_filename', n.get_str_value()),
            "do_not_proceed_until": lambda n : setattr(self, 'do_not_proceed_until', n.get_object_value(TeamsSetupGuide_do_not_proceed_until)),
            "manifest_url": lambda n : setattr(self, 'manifest_url', n.get_str_value()),
            "messages_url": lambda n : setattr(self, 'messages_url', n.get_str_value()),
            "preflight_questions": lambda n : setattr(self, 'preflight_questions', n.get_collection_of_primitive_values(str)),
            "provider": lambda n : setattr(self, 'provider', n.get_str_value()),
            "recommended_bot_type": lambda n : setattr(self, 'recommended_bot_type', n.get_enum_value(TeamsSetupGuide_recommended_bot_type)),
            "required_credentials": lambda n : setattr(self, 'required_credentials', n.get_collection_of_enum_values(TeamsSetupGuide_required_credentials)),
            "steps": lambda n : setattr(self, 'steps', n.get_collection_of_primitive_values(str)),
            "token_scope": lambda n : setattr(self, 'token_scope', n.get_str_value()),
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
        writer.write_str_value("default_package_filename", self.default_package_filename)
        writer.write_object_value("do_not_proceed_until", self.do_not_proceed_until)
        writer.write_str_value("manifest_url", self.manifest_url)
        writer.write_str_value("messages_url", self.messages_url)
        writer.write_collection_of_primitive_values("preflight_questions", self.preflight_questions)
        writer.write_str_value("provider", self.provider)
        writer.write_enum_value("recommended_bot_type", self.recommended_bot_type)
        writer.write_collection_of_enum_values("required_credentials", self.required_credentials)
        writer.write_collection_of_primitive_values("steps", self.steps)
        writer.write_str_value("token_scope", self.token_scope)
    

