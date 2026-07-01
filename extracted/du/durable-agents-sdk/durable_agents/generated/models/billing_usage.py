from __future__ import annotations
import datetime
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.serialization import Parsable, ParseNode, SerializationWriter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .billing_usage_provider_kind import BillingUsage_provider_kind
    from .billing_usage_status import BillingUsage_status

@dataclass
class BillingUsage(Parsable):
    # The admin_grant_credits property
    admin_grant_credits: Optional[float] = None
    # The available_balance_usd property
    available_balance_usd: Optional[float] = None
    # The available_credits property
    available_credits: Optional[float] = None
    # The created_at property
    created_at: Optional[datetime.datetime] = None
    # The credit_value_usd property
    credit_value_usd: Optional[float] = None
    # The grant_credits property
    grant_credits: Optional[float] = None
    # The last_graphlit_sync_at property
    last_graphlit_sync_at: Optional[datetime.datetime] = None
    # The owner property
    owner: Optional[str] = None
    # The provider_customer_id property
    provider_customer_id: Optional[str] = None
    # The provider_kind property
    provider_kind: Optional[BillingUsage_provider_kind] = None
    # The purchased_credits property
    purchased_credits: Optional[float] = None
    # The reserved_credits property
    reserved_credits: Optional[float] = None
    # The signup_grant_credits property
    signup_grant_credits: Optional[float] = None
    # The status property
    status: Optional[BillingUsage_status] = None
    # The total_credits property
    total_credits: Optional[float] = None
    # The updated_at property
    updated_at: Optional[datetime.datetime] = None
    # The used_credits property
    used_credits: Optional[float] = None
    
    @staticmethod
    def create_from_discriminator_value(parse_node: ParseNode) -> BillingUsage:
        """
        Creates a new instance of the appropriate class based on discriminator value
        param parse_node: The parse node to use to read the discriminator value and create the object
        Returns: BillingUsage
        """
        if parse_node is None:
            raise TypeError("parse_node cannot be null.")
        return BillingUsage()
    
    def get_field_deserializers(self,) -> dict[str, Callable[[ParseNode], None]]:
        """
        The deserialization information for the current model
        Returns: dict[str, Callable[[ParseNode], None]]
        """
        from .billing_usage_provider_kind import BillingUsage_provider_kind
        from .billing_usage_status import BillingUsage_status

        from .billing_usage_provider_kind import BillingUsage_provider_kind
        from .billing_usage_status import BillingUsage_status

        fields: dict[str, Callable[[Any], None]] = {
            "admin_grant_credits": lambda n : setattr(self, 'admin_grant_credits', n.get_float_value()),
            "available_balance_usd": lambda n : setattr(self, 'available_balance_usd', n.get_float_value()),
            "available_credits": lambda n : setattr(self, 'available_credits', n.get_float_value()),
            "created_at": lambda n : setattr(self, 'created_at', n.get_datetime_value()),
            "credit_value_usd": lambda n : setattr(self, 'credit_value_usd', n.get_float_value()),
            "grant_credits": lambda n : setattr(self, 'grant_credits', n.get_float_value()),
            "last_graphlit_sync_at": lambda n : setattr(self, 'last_graphlit_sync_at', n.get_datetime_value()),
            "owner": lambda n : setattr(self, 'owner', n.get_str_value()),
            "provider_customer_id": lambda n : setattr(self, 'provider_customer_id', n.get_str_value()),
            "provider_kind": lambda n : setattr(self, 'provider_kind', n.get_enum_value(BillingUsage_provider_kind)),
            "purchased_credits": lambda n : setattr(self, 'purchased_credits', n.get_float_value()),
            "reserved_credits": lambda n : setattr(self, 'reserved_credits', n.get_float_value()),
            "signup_grant_credits": lambda n : setattr(self, 'signup_grant_credits', n.get_float_value()),
            "status": lambda n : setattr(self, 'status', n.get_enum_value(BillingUsage_status)),
            "total_credits": lambda n : setattr(self, 'total_credits', n.get_float_value()),
            "updated_at": lambda n : setattr(self, 'updated_at', n.get_datetime_value()),
            "used_credits": lambda n : setattr(self, 'used_credits', n.get_float_value()),
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
        writer.write_float_value("admin_grant_credits", self.admin_grant_credits)
        writer.write_float_value("available_balance_usd", self.available_balance_usd)
        writer.write_float_value("available_credits", self.available_credits)
        writer.write_datetime_value("created_at", self.created_at)
        writer.write_float_value("credit_value_usd", self.credit_value_usd)
        writer.write_float_value("grant_credits", self.grant_credits)
        writer.write_datetime_value("last_graphlit_sync_at", self.last_graphlit_sync_at)
        writer.write_str_value("owner", self.owner)
        writer.write_str_value("provider_customer_id", self.provider_customer_id)
        writer.write_enum_value("provider_kind", self.provider_kind)
        writer.write_float_value("purchased_credits", self.purchased_credits)
        writer.write_float_value("reserved_credits", self.reserved_credits)
        writer.write_float_value("signup_grant_credits", self.signup_grant_credits)
        writer.write_enum_value("status", self.status)
        writer.write_float_value("total_credits", self.total_credits)
        writer.write_datetime_value("updated_at", self.updated_at)
        writer.write_float_value("used_credits", self.used_credits)
    

