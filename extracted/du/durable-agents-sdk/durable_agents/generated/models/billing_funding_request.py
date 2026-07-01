from __future__ import annotations
import datetime
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.api_error import APIError
from kiota_abstractions.serialization import Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .billing_funding_line_item import BillingFundingLineItem
    from .billing_funding_link_cli import BillingFundingLinkCli
    from .billing_funding_link_mcp import BillingFundingLinkMcp
    from .billing_funding_merchant import BillingFundingMerchant
    from .billing_funding_mpp import BillingFundingMpp
    from .billing_funding_provider_result import BillingFundingProviderResult
    from .billing_funding_status import BillingFundingStatus
    from .billing_funding_total import BillingFundingTotal

@dataclass
class BillingFundingRequest(APIError, Parsable):
    # The amount_cents property
    amount_cents: Optional[int] = None
    # The completed_at property
    completed_at: Optional[datetime.datetime] = None
    # The context property
    context: Optional[str] = None
    # The created_at property
    created_at: Optional[datetime.datetime] = None
    # The credits property
    credits: Optional[float] = None
    # The currency property
    currency: Optional[str] = None
    # The expires_at property
    expires_at: Optional[datetime.datetime] = None
    # The failure_code property
    failure_code: Optional[str] = None
    # The failure_message property
    failure_message: Optional[str] = None
    # The id property
    id: Optional[str] = None
    # The line_items property
    line_items: Optional[list[BillingFundingLineItem]] = None
    # The link_cli property
    link_cli: Optional[BillingFundingLinkCli] = None
    # The link_mcp property
    link_mcp: Optional[BillingFundingLinkMcp] = None
    # The merchant property
    merchant: Optional[BillingFundingMerchant] = None
    # The mpp property
    mpp: Optional[BillingFundingMpp] = None
    # The provider_result property
    provider_result: Optional[BillingFundingProviderResult] = None
    # The status property
    status: Optional[BillingFundingStatus] = None
    # The totals property
    totals: Optional[list[BillingFundingTotal]] = None
    # The updated_at property
    updated_at: Optional[datetime.datetime] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> BillingFundingRequest:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: BillingFundingRequest
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return BillingFundingRequest()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        from .billing_funding_line_item import BillingFundingLineItem
        from .billing_funding_link_cli import BillingFundingLinkCli
        from .billing_funding_link_mcp import BillingFundingLinkMcp
        from .billing_funding_merchant import BillingFundingMerchant
        from .billing_funding_mpp import BillingFundingMpp
        from .billing_funding_provider_result import BillingFundingProviderResult
        from .billing_funding_status import BillingFundingStatus
        from .billing_funding_total import BillingFundingTotal

        from .billing_funding_line_item import BillingFundingLineItem
        from .billing_funding_link_cli import BillingFundingLinkCli
        from .billing_funding_link_mcp import BillingFundingLinkMcp
        from .billing_funding_merchant import BillingFundingMerchant
        from .billing_funding_mpp import BillingFundingMpp
        from .billing_funding_provider_result import BillingFundingProviderResult
        from .billing_funding_status import BillingFundingStatus
        from .billing_funding_total import BillingFundingTotal

        fields: dict[str, Callable[[Any], None]] = {
            "amount_cents": lambda n : setattr(self, 'amount_cents', n.get_int_value()),
            "completed_at": lambda n : setattr(self, 'completed_at', n.get_datetime_value()),
            "context": lambda n : setattr(self, 'context', n.get_str_value()),
            "created_at": lambda n : setattr(self, 'created_at', n.get_datetime_value()),
            "credits": lambda n : setattr(self, 'credits', n.get_float_value()),
            "currency": lambda n : setattr(self, 'currency', n.get_str_value()),
            "expires_at": lambda n : setattr(self, 'expires_at', n.get_datetime_value()),
            "failure_code": lambda n : setattr(self, 'failure_code', n.get_str_value()),
            "failure_message": lambda n : setattr(self, 'failure_message', n.get_str_value()),
            "id": lambda n : setattr(self, 'id', n.get_str_value()),
            "line_items": lambda n : setattr(self, 'line_items', n.get_collection_of_object_values(BillingFundingLineItem)),
            "link_cli": lambda n : setattr(self, 'link_cli', n.get_object_value(BillingFundingLinkCli)),
            "link_mcp": lambda n : setattr(self, 'link_mcp', n.get_object_value(BillingFundingLinkMcp)),
            "merchant": lambda n : setattr(self, 'merchant', n.get_object_value(BillingFundingMerchant)),
            "mpp": lambda n : setattr(self, 'mpp', n.get_object_value(BillingFundingMpp)),
            "provider_result": lambda n : setattr(self, 'provider_result', n.get_object_value(BillingFundingProviderResult)),
            "status": lambda n : setattr(self, 'status', n.get_enum_value(BillingFundingStatus)),
            "totals": lambda n : setattr(self, 'totals', n.get_collection_of_object_values(BillingFundingTotal)),
            "updated_at": lambda n : setattr(self, 'updated_at', n.get_datetime_value()),
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
        writer.write_int_value("amount_cents", self.amount_cents)
        writer.write_datetime_value("completed_at", self.completed_at)
        writer.write_str_value("context", self.context)
        writer.write_datetime_value("created_at", self.created_at)
        writer.write_float_value("credits", self.credits)
        writer.write_str_value("currency", self.currency)
        writer.write_datetime_value("expires_at", self.expires_at)
        writer.write_str_value("failure_code", self.failure_code)
        writer.write_str_value("failure_message", self.failure_message)
        writer.write_str_value("id", self.id)
        writer.write_collection_of_object_values("line_items", self.line_items)
        writer.write_object_value("link_cli", self.link_cli)
        writer.write_object_value("link_mcp", self.link_mcp)
        writer.write_object_value("merchant", self.merchant)
        writer.write_object_value("mpp", self.mpp)
        writer.write_object_value("provider_result", self.provider_result)
        writer.write_enum_value("status", self.status)
        writer.write_collection_of_object_values("totals", self.totals)
        writer.write_datetime_value("updated_at", self.updated_at)
    
    @property
    def primary_message(self) -> Optional[str]:
        """
        The primary error message.
        """
        return super().message

