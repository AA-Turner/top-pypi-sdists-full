from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .billing_funding_line_item import BillingFundingLineItem
    from .billing_funding_total import BillingFundingTotal

@dataclass
class BillingFundingLinkMcp_spend_request_create_input_withou_0f14b056(Parsable):
    """
    Original name: BillingFundingLinkMcp_spend_request_create_input_without_payment_method
    """
    # The amount property
    amount: Optional[int] = None
    # The context property
    context: Optional[str] = None
    # The credentialType property
    credential_type: Optional[str] = None
    # The currency property
    currency: Optional[str] = None
    # The lineItem property
    line_item: Optional[list[BillingFundingLineItem]] = None
    # The networkId property
    network_id: Optional[str] = None
    # The requestApproval property
    request_approval: Optional[bool] = None
    # The total property
    total: Optional[list[BillingFundingTotal]] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> BillingFundingLinkMcp_spend_request_create_input_withou_0f14b056:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: BillingFundingLinkMcp_spend_request_create_input_withou_0f14b056
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return BillingFundingLinkMcp_spend_request_create_input_withou_0f14b056()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        from .billing_funding_line_item import BillingFundingLineItem
        from .billing_funding_total import BillingFundingTotal

        from .billing_funding_line_item import BillingFundingLineItem
        from .billing_funding_total import BillingFundingTotal

        fields: dict[str, Callable[[Any], None]] = {
            "amount": lambda n : setattr(self, 'amount', n.get_int_value()),
            "context": lambda n : setattr(self, 'context', n.get_str_value()),
            "credentialType": lambda n : setattr(self, 'credential_type', n.get_str_value()),
            "currency": lambda n : setattr(self, 'currency', n.get_str_value()),
            "lineItem": lambda n : setattr(self, 'line_item', n.get_collection_of_object_values(BillingFundingLineItem)),
            "networkId": lambda n : setattr(self, 'network_id', n.get_str_value()),
            "requestApproval": lambda n : setattr(self, 'request_approval', n.get_bool_value()),
            "total": lambda n : setattr(self, 'total', n.get_collection_of_object_values(BillingFundingTotal)),
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
        writer.write_int_value("amount", self.amount)
        writer.write_str_value("context", self.context)
        writer.write_str_value("credentialType", self.credential_type)
        writer.write_str_value("currency", self.currency)
        writer.write_collection_of_object_values("lineItem", self.line_item)
        writer.write_str_value("networkId", self.network_id)
        writer.write_bool_value("requestApproval", self.request_approval)
        writer.write_collection_of_object_values("total", self.total)
    

