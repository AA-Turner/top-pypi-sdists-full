from collections.abc import Mapping
from typing import Any, TypeVar, Union
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ComponentUserUsageLimitRequest")


@_attrs_define
class ComponentUserUsageLimitRequest:
    """
    Attributes:
        resource (str):
        component (UUID):
        user (str):
        limit (Union[Unset, str]):
    """

    resource: str
    component: UUID
    user: str
    limit: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        resource = self.resource

        component = str(self.component)

        user = self.user

        limit = self.limit

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "resource": resource,
                "component": component,
                "user": user,
            }
        )
        if limit is not UNSET:
            field_dict["limit"] = limit

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        resource = d.pop("resource")

        component = UUID(d.pop("component"))

        user = d.pop("user")

        limit = d.pop("limit", UNSET)

        component_user_usage_limit_request = cls(
            resource=resource,
            component=component,
            user=user,
            limit=limit,
        )

        component_user_usage_limit_request.additional_properties = d
        return component_user_usage_limit_request

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
