from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

@dataclass
class BillingFundingLinkCli_mpp_pay(Parsable):
    # The args_without_spend_request_id property
    args_without_spend_request_id: Optional[list[str]] = None
    # The spend_request_id_required property
    spend_request_id_required: Optional[bool] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> BillingFundingLinkCli_mpp_pay:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: BillingFundingLinkCli_mpp_pay
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return BillingFundingLinkCli_mpp_pay()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        fields: dict[str, Callable[[Any], None]] = {
            "args_without_spend_request_id": lambda n : setattr(self, 'args_without_spend_request_id', n.get_collection_of_primitive_values(str)),
            "spend_request_id_required": lambda n : setattr(self, 'spend_request_id_required', n.get_bool_value()),
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
        writer.write_collection_of_primitive_values("args_without_spend_request_id", self.args_without_spend_request_id)
        writer.write_bool_value("spend_request_id_required", self.spend_request_id_required)
    

