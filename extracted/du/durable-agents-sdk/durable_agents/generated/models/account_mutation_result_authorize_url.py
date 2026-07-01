from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import ComposedTypeWrapper, Parsable, ParseNode, ParseNodeHelper, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .account_mutation_result_authorize_url_member1 import AccountMutationResult_authorize_urlMember1

@dataclass
class AccountMutationResult_authorize_url(ComposedTypeWrapper, Parsable):
    """
    Composed type wrapper for classes AccountMutationResult_authorize_urlMember1, str
    """
    # Composed type representation for type AccountMutationResult_authorize_urlMember1
    account_mutation_result_authorize_url_member1: Optional[AccountMutationResult_authorize_urlMember1] = None
    # Composed type representation for type str
    string: Optional[str] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> AccountMutationResult_authorize_url:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: AccountMutationResult_authorize_url
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        result = AccountMutationResult_authorize_url()
        if string_value := parse_node.get_str_value():
            result.string = string_value
        else:
            from .account_mutation_result_authorize_url_member1 import AccountMutationResult_authorize_urlMember1

            result.account_mutation_result_authorize_url_member1 = AccountMutationResult_authorize_urlMember1()
        return result
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        from .account_mutation_result_authorize_url_member1 import AccountMutationResult_authorize_urlMember1

        if self.account_mutation_result_authorize_url_member1:
            return ParseNodeHelper.merge_deserializers_for_intersection_wrapper(self.account_mutation_result_authorize_url_member1)
        return {}
    
    def serialize(self,writer: SerializationWriter) -> None:
        """
        Serializes information the current object
        param writer: Serialization writer to use to serialize this model
        Returns: None
        """
        if writer is None:
            raise TypeError("writer cannot be null.")
        if self.string:
            writer.write_str_value(None, self.string)
        else:
            writer.write_object_value(None, self.account_mutation_result_authorize_url_member1)
    

