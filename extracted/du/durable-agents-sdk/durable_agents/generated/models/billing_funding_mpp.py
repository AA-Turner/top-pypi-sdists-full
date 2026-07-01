from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .billing_funding_mpp_body import BillingFundingMpp_body

@dataclass
class BillingFundingMpp(Parsable):
    # The body property
    body: Optional[BillingFundingMpp_body] = None
    # The challenge property
    challenge: Optional[str] = None
    # The debug_decode_command property
    debug_decode_command: Optional[str] = None
    # The method property
    method: Optional[str] = None
    # The network_id property
    network_id: Optional[str] = None
    # The pay_command property
    pay_command: Optional[str] = None
    # The url property
    url: Optional[str] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> BillingFundingMpp:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: BillingFundingMpp
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return BillingFundingMpp()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        from .billing_funding_mpp_body import BillingFundingMpp_body

        from .billing_funding_mpp_body import BillingFundingMpp_body

        fields: dict[str, Callable[[Any], None]] = {
            "body": lambda n : setattr(self, 'body', n.get_object_value(BillingFundingMpp_body)),
            "challenge": lambda n : setattr(self, 'challenge', n.get_str_value()),
            "debug_decode_command": lambda n : setattr(self, 'debug_decode_command', n.get_str_value()),
            "method": lambda n : setattr(self, 'method', n.get_str_value()),
            "network_id": lambda n : setattr(self, 'network_id', n.get_str_value()),
            "pay_command": lambda n : setattr(self, 'pay_command', n.get_str_value()),
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
        writer.write_object_value("body", self.body)
        writer.write_str_value("challenge", self.challenge)
        writer.write_str_value("debug_decode_command", self.debug_decode_command)
        writer.write_str_value("method", self.method)
        writer.write_str_value("network_id", self.network_id)
        writer.write_str_value("pay_command", self.pay_command)
        writer.write_str_value("url", self.url)
    

