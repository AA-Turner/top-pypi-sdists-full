from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

@dataclass
class BillingFundingLinkCli_spend_request_create(Parsable):
    # The args_without_payment_method property
    args_without_payment_method: Optional[list[str]] = None
    # The payment_method_id_required property
    payment_method_id_required: Optional[bool] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> BillingFundingLinkCli_spend_request_create:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: BillingFundingLinkCli_spend_request_create
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return BillingFundingLinkCli_spend_request_create()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        fields: dict[str, Callable[[Any], None]] = {
            "args_without_payment_method": lambda n : setattr(self, 'args_without_payment_method', n.get_collection_of_primitive_values(str)),
            "payment_method_id_required": lambda n : setattr(self, 'payment_method_id_required', n.get_bool_value()),
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
        writer.write_collection_of_primitive_values("args_without_payment_method", self.args_without_payment_method)
        writer.write_bool_value("payment_method_id_required", self.payment_method_id_required)
    

