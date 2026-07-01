from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

@dataclass
class TeamsConnectorSecrets(Parsable):
    # The bot_id property
    bot_id: Optional[str] = None
    # The bot_password property
    bot_password: Optional[str] = None
    # The tenant_id property
    tenant_id: Optional[str] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> TeamsConnectorSecrets:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: TeamsConnectorSecrets
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return TeamsConnectorSecrets()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        fields: dict[str, Callable[[Any], None]] = {
            "bot_id": lambda n : setattr(self, 'bot_id', n.get_str_value()),
            "bot_password": lambda n : setattr(self, 'bot_password', n.get_str_value()),
            "tenant_id": lambda n : setattr(self, 'tenant_id', n.get_str_value()),
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
        writer.write_str_value("bot_id", self.bot_id)
        writer.write_str_value("bot_password", self.bot_password)
        writer.write_str_value("tenant_id", self.tenant_id)
    

