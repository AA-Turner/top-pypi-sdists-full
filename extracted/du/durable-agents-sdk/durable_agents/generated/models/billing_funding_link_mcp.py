from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .billing_funding_link_mcp_mpp_pay_input_without_spend_request_id import BillingFundingLinkMcp_mpp_pay_input_without_spend_request_id
    from .billing_funding_link_mcp_spend_request_create_input_withou_0f14b056 import BillingFundingLinkMcp_spend_request_create_input_withou_0f14b056

@dataclass
class BillingFundingLinkMcp(Parsable):
    # The mpp_pay_input_without_spend_request_id property
    mpp_pay_input_without_spend_request_id: Optional[BillingFundingLinkMcp_mpp_pay_input_without_spend_request_id] = None
    # The spend_request_create_input_without_payment_method property
    spend_request_create_input_without_payment_method: Optional[BillingFundingLinkMcp_spend_request_create_input_withou_0f14b056] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> BillingFundingLinkMcp:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: BillingFundingLinkMcp
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return BillingFundingLinkMcp()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        from .billing_funding_link_mcp_mpp_pay_input_without_spend_request_id import BillingFundingLinkMcp_mpp_pay_input_without_spend_request_id
        from .billing_funding_link_mcp_spend_request_create_input_withou_0f14b056 import BillingFundingLinkMcp_spend_request_create_input_withou_0f14b056

        from .billing_funding_link_mcp_mpp_pay_input_without_spend_request_id import BillingFundingLinkMcp_mpp_pay_input_without_spend_request_id
        from .billing_funding_link_mcp_spend_request_create_input_withou_0f14b056 import BillingFundingLinkMcp_spend_request_create_input_withou_0f14b056

        fields: dict[str, Callable[[Any], None]] = {
            "mpp_pay_input_without_spend_request_id": lambda n : setattr(self, 'mpp_pay_input_without_spend_request_id', n.get_object_value(BillingFundingLinkMcp_mpp_pay_input_without_spend_request_id)),
            "spend_request_create_input_without_payment_method": lambda n : setattr(self, 'spend_request_create_input_without_payment_method', n.get_object_value(BillingFundingLinkMcp_spend_request_create_input_withou_0f14b056)),
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
        writer.write_object_value("mpp_pay_input_without_spend_request_id", self.mpp_pay_input_without_spend_request_id)
        writer.write_object_value("spend_request_create_input_without_payment_method", self.spend_request_create_input_without_payment_method)
    

