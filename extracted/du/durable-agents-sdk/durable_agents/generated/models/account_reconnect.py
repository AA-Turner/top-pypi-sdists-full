from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .account_o_auth_profile import AccountOAuthProfile

@dataclass
class AccountReconnect(Parsable):
    # OAuth permission profile. `context` requests read/default scopes; `delivery` requests read scopes plus action/write scopes.
    oauth_profile: Optional[AccountOAuthProfile] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> AccountReconnect:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: AccountReconnect
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return AccountReconnect()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        from .account_o_auth_profile import AccountOAuthProfile

        from .account_o_auth_profile import AccountOAuthProfile

        fields: dict[str, Callable[[Any], None]] = {
            "oauth_profile": lambda n : setattr(self, 'oauth_profile', n.get_enum_value(AccountOAuthProfile)),
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
        writer.write_enum_value("oauth_profile", self.oauth_profile)
    

