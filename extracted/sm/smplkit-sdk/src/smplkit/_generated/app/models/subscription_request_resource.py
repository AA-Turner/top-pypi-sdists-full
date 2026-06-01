from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.subscription_request_resource_type import check_subscription_request_resource_type
from ..models.subscription_request_resource_type import SubscriptionRequestResourceType
from typing import cast

if TYPE_CHECKING:
    from ..models.subscription_request_attributes import SubscriptionRequestAttributes


T = TypeVar("T", bound="SubscriptionRequestResource")


@_attrs_define
class SubscriptionRequestResource:
    """JSON:API resource object for a subscription update request.

    Example:
        {'attributes': {'items': [{'plan': 'pro', 'product': 'audit'}, {'plan': 'pro', 'product': 'config'}],
            'payment_method': 'p1q2r3s4-5678-90ab-cdef-1234567890ab'}, 'type': 'subscription'}

    Attributes:
        type_ (SubscriptionRequestResourceType): JSON:API resource type.
        attributes (SubscriptionRequestAttributes): Customer's desired subscription state.
        id (None | str | Unset): Subscription identifier; the server ignores this and uses the auth context.
    """

    type_: SubscriptionRequestResourceType
    attributes: SubscriptionRequestAttributes
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
        from ..models.subscription_request_attributes import SubscriptionRequestAttributes

        d = dict(src_dict)
        type_ = check_subscription_request_resource_type(d.pop("type"))

        attributes = SubscriptionRequestAttributes.from_dict(d.pop("attributes"))

        def _parse_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        id = _parse_id(d.pop("id", UNSET))

        subscription_request_resource = cls(
            type_=type_,
            attributes=attributes,
            id=id,
        )

        subscription_request_resource.additional_properties = d
        return subscription_request_resource

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
