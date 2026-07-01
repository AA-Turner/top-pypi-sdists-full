from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .account import Account
    from .account_mutation_result_authorize_url import AccountMutationResult_authorize_url

@dataclass
class AccountMutationResult(Parsable):
    # The account property
    account: Optional[Account] = None
    # The authorization_required property
    authorization_required: Optional[bool] = None
    # The authorize_url property
    authorize_url: Optional[AccountMutationResult_authorize_url] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> AccountMutationResult:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: AccountMutationResult
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return AccountMutationResult()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        from .account import Account
        from .account_mutation_result_authorize_url import AccountMutationResult_authorize_url

        from .account import Account
        from .account_mutation_result_authorize_url import AccountMutationResult_authorize_url

        fields: dict[str, Callable[[Any], None]] = {
            "account": lambda n : setattr(self, 'account', n.get_object_value(Account)),
            "authorization_required": lambda n : setattr(self, 'authorization_required', n.get_bool_value()),
            "authorize_url": lambda n : setattr(self, 'authorize_url', n.get_object_value(AccountMutationResult_authorize_url)),
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
        writer.write_object_value("account", self.account)
        writer.write_bool_value("authorization_required", self.authorization_required)
        writer.write_object_value("authorize_url", self.authorize_url)
    

