from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field


if TYPE_CHECKING:
    from ..models.admin_subscription_request_resource import AdminSubscriptionRequestResource


T = TypeVar("T", bound="AdminSubscriptionRequest")


@_attrs_define
class AdminSubscriptionRequest:
    """Admin-scope request envelope for replacing a subscription.

    Attributes:
        data (AdminSubscriptionRequestResource): Admin-scope resource object for a subscription update request. Example:
            {'attributes': {'discount_override_pct': 100, 'items': [{'plan': 'pro', 'product': 'audit'}]}, 'type':
            'subscription'}.
    """

    data: AdminSubscriptionRequestResource
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
        from ..models.admin_subscription_request_resource import AdminSubscriptionRequestResource

        d = dict(src_dict)
        data = AdminSubscriptionRequestResource.from_dict(d.pop("data"))

        admin_subscription_request = cls(
            data=data,
        )

        admin_subscription_request.additional_properties = d
        return admin_subscription_request

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
