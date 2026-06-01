from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field


if TYPE_CHECKING:
    from ..models.subscription_request_resource import SubscriptionRequestResource


T = TypeVar("T", bound="SubscriptionRequest")


@_attrs_define
class SubscriptionRequest:
    """Single-resource request envelope for replacing the subscription.

    Attributes:
        data (SubscriptionRequestResource): JSON:API resource object for a subscription update request. Example:
            {'attributes': {'items': [{'plan': 'pro', 'product': 'audit'}, {'plan': 'pro', 'product': 'config'}],
            'payment_method': 'p1q2r3s4-5678-90ab-cdef-1234567890ab'}, 'type': 'subscription'}.
    """

    data: SubscriptionRequestResource
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
        from ..models.subscription_request_resource import SubscriptionRequestResource

        d = dict(src_dict)
        data = SubscriptionRequestResource.from_dict(d.pop("data"))

        subscription_request = cls(
            data=data,
        )

        subscription_request.additional_properties = d
        return subscription_request

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
