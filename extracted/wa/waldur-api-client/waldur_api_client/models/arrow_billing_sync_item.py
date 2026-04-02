import datetime
from collections.abc import Mapping
from typing import Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

T = TypeVar("T", bound="ArrowBillingSyncItem")


@_attrs_define
class ArrowBillingSyncItem:
    """
    Attributes:
        uuid (UUID):
        arrow_line_reference (str): Arrow line ID
        invoice_item_uuid (UUID):
        original_price (str): Original price for reconciliation tracking
        compensation_item_uuid (UUID):
        vendor_name (str): Vendor name (e.g., Microsoft)
        subscription_reference (str): Arrow subscription reference
        classification (str): Classification (IAAS/SAAS)
        description (str): Line item description
        quantity (str): Quantity
        created (datetime.datetime):
    """

    uuid: UUID
    arrow_line_reference: str
    invoice_item_uuid: UUID
    original_price: str
    compensation_item_uuid: UUID
    vendor_name: str
    subscription_reference: str
    classification: str
    description: str
    quantity: str
    created: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid = str(self.uuid)

        arrow_line_reference = self.arrow_line_reference

        invoice_item_uuid = str(self.invoice_item_uuid)

        original_price = self.original_price

        compensation_item_uuid = str(self.compensation_item_uuid)

        vendor_name = self.vendor_name

        subscription_reference = self.subscription_reference

        classification = self.classification

        description = self.description

        quantity = self.quantity

        created = self.created.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uuid": uuid,
                "arrow_line_reference": arrow_line_reference,
                "invoice_item_uuid": invoice_item_uuid,
                "original_price": original_price,
                "compensation_item_uuid": compensation_item_uuid,
                "vendor_name": vendor_name,
                "subscription_reference": subscription_reference,
                "classification": classification,
                "description": description,
                "quantity": quantity,
                "created": created,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        uuid = UUID(d.pop("uuid"))

        arrow_line_reference = d.pop("arrow_line_reference")

        invoice_item_uuid = UUID(d.pop("invoice_item_uuid"))

        original_price = d.pop("original_price")

        compensation_item_uuid = UUID(d.pop("compensation_item_uuid"))

        vendor_name = d.pop("vendor_name")

        subscription_reference = d.pop("subscription_reference")

        classification = d.pop("classification")

        description = d.pop("description")

        quantity = d.pop("quantity")

        created = isoparse(d.pop("created"))

        arrow_billing_sync_item = cls(
            uuid=uuid,
            arrow_line_reference=arrow_line_reference,
            invoice_item_uuid=invoice_item_uuid,
            original_price=original_price,
            compensation_item_uuid=compensation_item_uuid,
            vendor_name=vendor_name,
            subscription_reference=subscription_reference,
            classification=classification,
            description=description,
            quantity=quantity,
            created=created,
        )

        arrow_billing_sync_item.additional_properties = d
        return arrow_billing_sync_item

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
