from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .account_o_auth_profile import AccountOAuthProfile
    from .account_provider import AccountProvider

@dataclass
class AccountCreate(Parsable):
    # OAuth permission profile. `context` requests read/default scopes; `delivery` requests read scopes plus action/write scopes.
    oauth_profile: Optional[AccountOAuthProfile] = None
    # The provider property
    provider: Optional[AccountProvider] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> AccountCreate:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: AccountCreate
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return AccountCreate()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        from .account_o_auth_profile import AccountOAuthProfile
        from .account_provider import AccountProvider

        from .account_o_auth_profile import AccountOAuthProfile
        from .account_provider import AccountProvider

        fields: dict[str, Callable[[Any], None]] = {
            "oauth_profile": lambda n : setattr(self, 'oauth_profile', n.get_enum_value(AccountOAuthProfile)),
            "provider": lambda n : setattr(self, 'provider', n.get_enum_value(AccountProvider)),
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
        writer.write_enum_value("provider", self.provider)
    

