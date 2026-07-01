from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .billing_funding_link_cli_mpp_pay import BillingFundingLinkCli_mpp_pay
    from .billing_funding_link_cli_spend_request_create import BillingFundingLinkCli_spend_request_create

@dataclass
class BillingFundingLinkCli(Parsable):
    # The mpp_pay property
    mpp_pay: Optional[BillingFundingLinkCli_mpp_pay] = None
    # The spend_request_create property
    spend_request_create: Optional[BillingFundingLinkCli_spend_request_create] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> BillingFundingLinkCli:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: BillingFundingLinkCli
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return BillingFundingLinkCli()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        from .billing_funding_link_cli_mpp_pay import BillingFundingLinkCli_mpp_pay
        from .billing_funding_link_cli_spend_request_create import BillingFundingLinkCli_spend_request_create

        from .billing_funding_link_cli_mpp_pay import BillingFundingLinkCli_mpp_pay
        from .billing_funding_link_cli_spend_request_create import BillingFundingLinkCli_spend_request_create

        fields: dict[str, Callable[[Any], None]] = {
            "mpp_pay": lambda n : setattr(self, 'mpp_pay', n.get_object_value(BillingFundingLinkCli_mpp_pay)),
            "spend_request_create": lambda n : setattr(self, 'spend_request_create', n.get_object_value(BillingFundingLinkCli_spend_request_create)),
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
        writer.write_object_value("mpp_pay", self.mpp_pay)
        writer.write_object_value("spend_request_create", self.spend_request_create)
    

