from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field


if TYPE_CHECKING:
    from ..models.subscription_resource import SubscriptionResource


T = TypeVar("T", bound="SubscriptionResponse")


@_attrs_define
class SubscriptionResponse:
    """Single-resource response envelope for a subscription.

    Attributes:
        data (SubscriptionResource): JSON:API resource object for a subscription. Example: {'attributes':
            {'current_period_end': '2026-06-01T00:00:00Z', 'current_period_start': '2026-05-01T00:00:00Z',
            'discount_amount_cents': 2220, 'discount_pct': 15, 'discount_source': 'VOLUME', 'items': [{'id':
            'i1j2k3l4-5678-90ab-cdef-1234567890ab', 'plan': 'pro', 'price_monthly_cents': 9900, 'product': 'audit'}],
            'next_tier': {'additional_savings_cents': 4281, 'discount_pct': 33, 'products_needed': 1}, 'payment_method':
            'p1q2r3s4-5678-90ab-cdef-1234567890ab', 'status': 'ACTIVE', 'subtotal_cents': 14800, 'total_cents': 12580},
            'id': 'a1b2c3d4-e5f6-7890-abcd-ef1234567890', 'type': 'subscription'}.
    """

    data: SubscriptionResource
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
        from ..models.subscription_resource import SubscriptionResource

        d = dict(src_dict)
        data = SubscriptionResource.from_dict(d.pop("data"))

        subscription_response = cls(
            data=data,
        )

        subscription_response.additional_properties = d
        return subscription_response

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
