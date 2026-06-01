from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field


if TYPE_CHECKING:
    from ..models.subscription_preview_resource import SubscriptionPreviewResource


T = TypeVar("T", bound="SubscriptionPreviewResponse")


@_attrs_define
class SubscriptionPreviewResponse:
    """Response envelope for the preview action.

    Attributes:
        data (SubscriptionPreviewResource): JSON:API resource object for a subscription preview. Example: {'attributes':
            {'changes': [{'effect': 'IMMEDIATE', 'from_plan': 'free', 'monthly_cents': 9900, 'product': 'audit',
            'prorated_charge_today_cents': 4521, 'to_plan': 'pro'}], 'next_invoice_total_cents': 12580,
            'projected_discount_amount_cents': 2220, 'projected_discount_pct': 15, 'projected_discount_source': 'VOLUME',
            'projected_subtotal_cents': 14800, 'projected_total_cents': 12580, 'total_charge_today_cents': 4521}, 'id':
            'preview', 'type': 'subscription_preview'}.
    """

    data: SubscriptionPreviewResource
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        data = self.data.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "data": data,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.subscription_preview_resource import SubscriptionPreviewResource

        d = dict(src_dict)
        data = SubscriptionPreviewResource.from_dict(d.pop("data"))

        subscription_preview_response = cls(
            data=data,
        )

        subscription_preview_response.additional_properties = d
        return subscription_preview_response

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
