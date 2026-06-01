from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.subscription_preview_resource_id import check_subscription_preview_resource_id
from ..models.subscription_preview_resource_id import SubscriptionPreviewResourceId
from ..models.subscription_preview_resource_type import check_subscription_preview_resource_type
from ..models.subscription_preview_resource_type import SubscriptionPreviewResourceType

if TYPE_CHECKING:
    from ..models.subscription_preview_attributes import SubscriptionPreviewAttributes


T = TypeVar("T", bound="SubscriptionPreviewResource")


@_attrs_define
class SubscriptionPreviewResource:
    """JSON:API resource object for a subscription preview.

    Example:
        {'attributes': {'changes': [{'effect': 'IMMEDIATE', 'from_plan': 'free', 'monthly_cents': 9900, 'product':
            'audit', 'prorated_charge_today_cents': 4521, 'to_plan': 'pro'}], 'next_invoice_total_cents': 12580,
            'projected_discount_amount_cents': 2220, 'projected_discount_pct': 15, 'projected_discount_source': 'VOLUME',
            'projected_subtotal_cents': 14800, 'projected_total_cents': 12580, 'total_charge_today_cents': 4521}, 'id':
            'preview', 'type': 'subscription_preview'}

    Attributes:
        type_ (SubscriptionPreviewResourceType): JSON:API resource type.
        attributes (SubscriptionPreviewAttributes): Projected totals and per-change breakdown for a hypothetical change.
        id (SubscriptionPreviewResourceId | Unset): Always `preview`. Default: 'preview'.
    """

    type_: SubscriptionPreviewResourceType
    attributes: SubscriptionPreviewAttributes
    id: SubscriptionPreviewResourceId | Unset = "preview"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        type_: str = self.type_

        attributes = self.attributes.to_dict()

        id: str | Unset = UNSET
        if not isinstance(self.id, Unset):
            id = self.id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type_,
                "attributes": attributes,
            }
        )
        if id is not UNSET:
            field_dict["id"] = id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.subscription_preview_attributes import SubscriptionPreviewAttributes

        d = dict(src_dict)
        type_ = check_subscription_preview_resource_type(d.pop("type"))

        attributes = SubscriptionPreviewAttributes.from_dict(d.pop("attributes"))

        _id = d.pop("id", UNSET)
        id: SubscriptionPreviewResourceId | Unset
        if isinstance(_id, Unset):
            id = UNSET
        else:
            id = check_subscription_preview_resource_id(_id)

        subscription_preview_resource = cls(
            type_=type_,
            attributes=attributes,
            id=id,
        )

        subscription_preview_resource.additional_properties = d
        return subscription_preview_resource

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
