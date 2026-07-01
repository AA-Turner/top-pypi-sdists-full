from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

@dataclass
class BillingFundingLinkMcp_mpp_pay_input_without_spend_request_id(Parsable):
    # The data property
    data: Optional[str] = None
    # The method property
    method: Optional[str] = None
    # The url property
    url: Optional[str] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> BillingFundingLinkMcp_mpp_pay_input_without_spend_request_id:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: BillingFundingLinkMcp_mpp_pay_input_without_spend_request_id
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return BillingFundingLinkMcp_mpp_pay_input_without_spend_request_id()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        fields: dict[str, Callable[[Any], None]] = {
            "data": lambda n : setattr(self, 'data', n.get_str_value()),
            "method": lambda n : setattr(self, 'method', n.get_str_value()),
            "url": lambda n : setattr(self, 'url', n.get_str_value()),
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
        writer.write_str_value("data", self.data)
        writer.write_str_value("method", self.method)
        writer.write_str_value("url", self.url)
    

