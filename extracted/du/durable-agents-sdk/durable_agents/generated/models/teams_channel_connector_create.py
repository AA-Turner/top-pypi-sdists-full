from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .channel_message_access import ChannelMessageAccess
    from .teams_connector_secrets import TeamsConnectorSecrets

@dataclass
class TeamsChannelConnectorCreate(Parsable):
    # The message_access property
    message_access: Optional[ChannelMessageAccess] = None
    # The name property
    name: Optional[str] = None
    # The provider property
    provider: Optional[str] = None
    # The teams property
    teams: Optional[TeamsConnectorSecrets] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> TeamsChannelConnectorCreate:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: TeamsChannelConnectorCreate
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return TeamsChannelConnectorCreate()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        from .channel_message_access import ChannelMessageAccess
        from .teams_connector_secrets import TeamsConnectorSecrets

        from .channel_message_access import ChannelMessageAccess
        from .teams_connector_secrets import TeamsConnectorSecrets

        fields: dict[str, Callable[[Any], None]] = {
            "message_access": lambda n : setattr(self, 'message_access', n.get_enum_value(ChannelMessageAccess)),
            "name": lambda n : setattr(self, 'name', n.get_str_value()),
            "provider": lambda n : setattr(self, 'provider', n.get_str_value()),
            "teams": lambda n : setattr(self, 'teams', n.get_object_value(TeamsConnectorSecrets)),
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
        writer.write_enum_value("message_access", self.message_access)
        writer.write_str_value("name", self.name)
        writer.write_str_value("provider", self.provider)
        writer.write_object_value("teams", self.teams)
    

