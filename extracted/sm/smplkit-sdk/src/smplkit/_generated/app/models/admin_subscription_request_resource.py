from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.admin_subscription_request_resource_type import AdminSubscriptionRequestResourceType
from ..models.admin_subscription_request_resource_type import check_admin_subscription_request_resource_type
from typing import cast

if TYPE_CHECKING:
    from ..models.admin_subscription_request_attributes import AdminSubscriptionRequestAttributes


T = TypeVar("T", bound="AdminSubscriptionRequestResource")


@_attrs_define
class AdminSubscriptionRequestResource:
    """Admin-scope resource object for a subscription update request.

    Example:
        {'attributes': {'discount_override_pct': 100, 'items': [{'plan': 'pro', 'product': 'audit'}]}, 'type':
            'subscription'}

    Attributes:
        type_ (AdminSubscriptionRequestResourceType): JSON:API resource type.
        attributes (AdminSubscriptionRequestAttributes): Same as the customer request body plus the admin-only override
            field.
        id (None | str | Unset):
    """

    type_: AdminSubscriptionRequestResourceType
    attributes: AdminSubscriptionRequestAttributes
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
        from ..models.admin_subscription_request_attributes import AdminSubscriptionRequestAttributes

        d = dict(src_dict)
        type_ = check_admin_subscription_request_resource_type(d.pop("type"))

        attributes = AdminSubscriptionRequestAttributes.from_dict(d.pop("attributes"))

        def _parse_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        id = _parse_id(d.pop("id", UNSET))

        admin_subscription_request_resource = cls(
            type_=type_,
            attributes=attributes,
            id=id,
        )

        admin_subscription_request_resource.additional_properties = d
        return admin_subscription_request_resource

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
