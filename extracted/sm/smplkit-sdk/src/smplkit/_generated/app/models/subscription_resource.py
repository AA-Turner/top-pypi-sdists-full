from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.subscription_resource_type import check_subscription_resource_type
from ..models.subscription_resource_type import SubscriptionResourceType
from typing import cast

if TYPE_CHECKING:
    from ..models.subscription_response_attributes import SubscriptionResponseAttributes


T = TypeVar("T", bound="SubscriptionResource")


@_attrs_define
class SubscriptionResource:
    """JSON:API resource object for a subscription.

    Example:
        {'attributes': {'current_period_end': '2026-06-01T00:00:00Z', 'current_period_start': '2026-05-01T00:00:00Z',
            'discount_amount_cents': 2220, 'discount_pct': 15, 'discount_source': 'VOLUME', 'items': [{'id':
            'i1j2k3l4-5678-90ab-cdef-1234567890ab', 'plan': 'pro', 'price_monthly_cents': 9900, 'product': 'audit'}],
            'next_tier': {'additional_savings_cents': 4281, 'discount_pct': 33, 'products_needed': 1}, 'payment_method':
            'p1q2r3s4-5678-90ab-cdef-1234567890ab', 'status': 'ACTIVE', 'subtotal_cents': 14800, 'total_cents': 12580},
            'id': 'a1b2c3d4-e5f6-7890-abcd-ef1234567890', 'type': 'subscription'}

    Attributes:
        type_ (SubscriptionResourceType): JSON:API resource type.
        attributes (SubscriptionResponseAttributes): Customer's subscription as returned by the API.
        id (None | str | Unset): Subscription identifier. Always `current` on response; absent on create-style requests.
    """

    type_: SubscriptionResourceType
    attributes: SubscriptionResponseAttributes
    id: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        type_: str = self.type_

        attributes = self.attributes.to_dict()

        id: None | str | Unset
        if isinstance(self.id, Unset):
            id = UNSET
        else:
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
        from ..models.subscription_response_attributes import SubscriptionResponseAttributes

        d = dict(src_dict)
        type_ = check_subscription_resource_type(d.pop("type"))

        attributes = SubscriptionResponseAttributes.from_dict(d.pop("attributes"))

        def _parse_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        id = _parse_id(d.pop("id", UNSET))

        subscription_resource = cls(
            type_=type_,
            attributes=attributes,
            id=id,
        )

        subscription_resource.additional_properties = d
        return subscription_resource

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
