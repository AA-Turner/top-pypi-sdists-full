from collections.abc import Mapping
from typing import Any, TypeVar, Union
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ResourceAccessSubnet")


@_attrs_define
class ResourceAccessSubnet:
    """
    Attributes:
        uuid (UUID):
        inet (str):
        resource (str):
        resource_name (str):
        resource_backend_id (str):
        description (Union[Unset, str]):
    """

    uuid: UUID
    inet: str
    resource: str
    resource_name: str
    resource_backend_id: str
    description: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid = str(self.uuid)

        inet = self.inet

        resource = self.resource

        resource_name = self.resource_name

        resource_backend_id = self.resource_backend_id

        description = self.description

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uuid": uuid,
                "inet": inet,
                "resource": resource,
                "resource_name": resource_name,
                "resource_backend_id": resource_backend_id,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        uuid = UUID(d.pop("uuid"))

        inet = d.pop("inet")

        resource = d.pop("resource")

        resource_name = d.pop("resource_name")

        resource_backend_id = d.pop("resource_backend_id")

        description = d.pop("description", UNSET)

        resource_access_subnet = cls(
            uuid=uuid,
            inet=inet,
            resource=resource,
            resource_name=resource_name,
            resource_backend_id=resource_backend_id,
            description=description,
        )

        resource_access_subnet.additional_properties = d
        return resource_access_subnet

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
