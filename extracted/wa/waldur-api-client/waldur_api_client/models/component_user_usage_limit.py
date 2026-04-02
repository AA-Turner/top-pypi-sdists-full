from collections.abc import Mapping
from typing import Any, TypeVar, Union
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ComponentUserUsageLimit")


@_attrs_define
class ComponentUserUsageLimit:
    """
    Attributes:
        url (str):
        uuid (UUID):
        resource (str):
        component (UUID):
        component_type (str): Unique internal name of the measured unit, for example floating_ip.
        user (str):
        limit (Union[Unset, str]):
    """

    url: str
    uuid: UUID
    resource: str
    component: UUID
    component_type: str
    user: str
    limit: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        url = self.url

        uuid = str(self.uuid)

        resource = self.resource

        component = str(self.component)

        component_type = self.component_type

        user = self.user

        limit = self.limit

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "url": url,
                "uuid": uuid,
                "resource": resource,
                "component": component,
                "component_type": component_type,
                "user": user,
            }
        )
        if limit is not UNSET:
            field_dict["limit"] = limit

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        url = d.pop("url")

        uuid = UUID(d.pop("uuid"))

        resource = d.pop("resource")

        component = UUID(d.pop("component"))

        component_type = d.pop("component_type")

        user = d.pop("user")

        limit = d.pop("limit", UNSET)

        component_user_usage_limit = cls(
            url=url,
            uuid=uuid,
            resource=resource,
            component=component,
            component_type=component_type,
            user=user,
            limit=limit,
        )

        component_user_usage_limit.additional_properties = d
        return component_user_usage_limit

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
