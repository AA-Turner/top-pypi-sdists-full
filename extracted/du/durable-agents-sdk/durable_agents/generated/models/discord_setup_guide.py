from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .channel_message_access import ChannelMessageAccess
    from .discord_command_registration import DiscordCommandRegistration
    from .discord_permission_guide import DiscordPermissionGuide
    from .discord_setup_guide_do_not_proceed_until import DiscordSetupGuide_do_not_proceed_until
    from .discord_setup_guide_required_credentials import DiscordSetupGuide_required_credentials
    from .discord_setup_guide_scopes import DiscordSetupGuide_scopes

@dataclass
class DiscordSetupGuide(Parsable):
    # The command property
    command: Optional[DiscordCommandRegistration] = None
    # The default_command_name property
    default_command_name: Optional[str] = None
    # The default_command_option property
    default_command_option: Optional[str] = None
    # The do_not_proceed_until property
    do_not_proceed_until: Optional[DiscordSetupGuide_do_not_proceed_until] = None
    # The effective_message_access property
    effective_message_access: Optional[ChannelMessageAccess] = None
    # The interactions_url property
    interactions_url: Optional[str] = None
    # The invite_url property
    invite_url: Optional[str] = None
    # The message_access property
    message_access: Optional[ChannelMessageAccess] = None
    # The message_access_capabilities property
    message_access_capabilities: Optional[list[ChannelMessageAccess]] = None
    # The permission_notes property
    permission_notes: Optional[list[str]] = None
    # The permissions property
    permissions: Optional[DiscordPermissionGuide] = None
    # The preflight_questions property
    preflight_questions: Optional[list[str]] = None
    # The provider property
    provider: Optional[str] = None
    # The required_credentials property
    required_credentials: Optional[list[DiscordSetupGuide_required_credentials]] = None
    # The scopes property
    scopes: Optional[list[DiscordSetupGuide_scopes]] = None
    # The steps property
    steps: Optional[list[str]] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> DiscordSetupGuide:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: DiscordSetupGuide
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return DiscordSetupGuide()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        from .channel_message_access import ChannelMessageAccess
        from .discord_command_registration import DiscordCommandRegistration
        from .discord_permission_guide import DiscordPermissionGuide
        from .discord_setup_guide_do_not_proceed_until import DiscordSetupGuide_do_not_proceed_until
        from .discord_setup_guide_required_credentials import DiscordSetupGuide_required_credentials
        from .discord_setup_guide_scopes import DiscordSetupGuide_scopes

        from .channel_message_access import ChannelMessageAccess
        from .discord_command_registration import DiscordCommandRegistration
        from .discord_permission_guide import DiscordPermissionGuide
        from .discord_setup_guide_do_not_proceed_until import DiscordSetupGuide_do_not_proceed_until
        from .discord_setup_guide_required_credentials import DiscordSetupGuide_required_credentials
        from .discord_setup_guide_scopes import DiscordSetupGuide_scopes

        fields: dict[str, Callable[[Any], None]] = {
            "command": lambda n : setattr(self, 'command', n.get_object_value(DiscordCommandRegistration)),
            "default_command_name": lambda n : setattr(self, 'default_command_name', n.get_str_value()),
            "default_command_option": lambda n : setattr(self, 'default_command_option', n.get_str_value()),
            "do_not_proceed_until": lambda n : setattr(self, 'do_not_proceed_until', n.get_object_value(DiscordSetupGuide_do_not_proceed_until)),
            "effective_message_access": lambda n : setattr(self, 'effective_message_access', n.get_enum_value(ChannelMessageAccess)),
            "interactions_url": lambda n : setattr(self, 'interactions_url', n.get_str_value()),
            "invite_url": lambda n : setattr(self, 'invite_url', n.get_str_value()),
            "message_access": lambda n : setattr(self, 'message_access', n.get_enum_value(ChannelMessageAccess)),
            "message_access_capabilities": lambda n : setattr(self, 'message_access_capabilities', n.get_collection_of_enum_values(ChannelMessageAccess)),
            "permission_notes": lambda n : setattr(self, 'permission_notes', n.get_collection_of_primitive_values(str)),
            "permissions": lambda n : setattr(self, 'permissions', n.get_object_value(DiscordPermissionGuide)),
            "preflight_questions": lambda n : setattr(self, 'preflight_questions', n.get_collection_of_primitive_values(str)),
            "provider": lambda n : setattr(self, 'provider', n.get_str_value()),
            "required_credentials": lambda n : setattr(self, 'required_credentials', n.get_collection_of_enum_values(DiscordSetupGuide_required_credentials)),
            "scopes": lambda n : setattr(self, 'scopes', n.get_collection_of_enum_values(DiscordSetupGuide_scopes)),
            "steps": lambda n : setattr(self, 'steps', n.get_collection_of_primitive_values(str)),
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
        writer.write_object_value("command", self.command)
        writer.write_str_value("default_command_name", self.default_command_name)
        writer.write_str_value("default_command_option", self.default_command_option)
        writer.write_object_value("do_not_proceed_until", self.do_not_proceed_until)
        writer.write_enum_value("effective_message_access", self.effective_message_access)
        writer.write_str_value("interactions_url", self.interactions_url)
        writer.write_str_value("invite_url", self.invite_url)
        writer.write_enum_value("message_access", self.message_access)
        writer.write_collection_of_enum_values("message_access_capabilities", self.message_access_capabilities)
        writer.write_collection_of_primitive_values("permission_notes", self.permission_notes)
        writer.write_object_value("permissions", self.permissions)
        writer.write_collection_of_primitive_values("preflight_questions", self.preflight_questions)
        writer.write_str_value("provider", self.provider)
        writer.write_collection_of_enum_values("required_credentials", self.required_credentials)
        writer.write_collection_of_enum_values("scopes", self.scopes)
        writer.write_collection_of_primitive_values("steps", self.steps)
    

