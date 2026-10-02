from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="OfferingRole")


@_attrs_define
class OfferingRole:
    """
    Attributes:
        uuid (UUID):
        name (str):
        content_type (Union[None, str]):
        offering_uuid (Union[None, str]):
        offering_name (Union[None, str]):
        is_active (bool):
        permissions (list[str]):
        description (Union[Unset, str]):
    """

    uuid: UUID
    name: str
    content_type: Union[None, str]
    offering_uuid: Union[None, str]
    offering_name: Union[None, str]
    is_active: bool
    permissions: list[str]
    description: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid = str(self.uuid)

        name = self.name

        content_type: Union[None, str]
        content_type = self.content_type

        offering_uuid: Union[None, str]
        offering_uuid = self.offering_uuid

        offering_name: Union[None, str]
        offering_name = self.offering_name

        is_active = self.is_active

        permissions = self.permissions

        description = self.description

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uuid": uuid,
                "name": name,
                "content_type": content_type,
                "offering_uuid": offering_uuid,
                "offering_name": offering_name,
                "is_active": is_active,
                "permissions": permissions,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        uuid = UUID(d.pop("uuid"))

        name = d.pop("name")

        def _parse_content_type(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        content_type = _parse_content_type(d.pop("content_type"))

        def _parse_offering_uuid(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        offering_uuid = _parse_offering_uuid(d.pop("offering_uuid"))

        def _parse_offering_name(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        offering_name = _parse_offering_name(d.pop("offering_name"))

        is_active = d.pop("is_active")

        permissions = cast(list[str], d.pop("permissions"))

        description = d.pop("description", UNSET)

        offering_role = cls(
            uuid=uuid,
            name=name,
            content_type=content_type,
            offering_uuid=offering_uuid,
            offering_name=offering_name,
            is_active=is_active,
            permissions=permissions,
            description=description,
        )

        offering_role.additional_properties = d
        return offering_role

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
