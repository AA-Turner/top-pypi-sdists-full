from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="RoleAvailabilityDetails")


@_attrs_define
class RoleAvailabilityDetails:
    """
    Attributes:
        uuid (UUID):
        role_uuid (UUID):
        role_name (str):
        role_content_type (Union[None, str]):
        scope_type (Union[None, str]):
        scope_uuid (Union[None, str]):
        scope_name (Union[None, str]):
        is_profile_managed (bool):
        profile_uuid (Union[None, str]):
        profile_name (Union[None, str]):
    """

    uuid: UUID
    role_uuid: UUID
    role_name: str
    role_content_type: Union[None, str]
    scope_type: Union[None, str]
    scope_uuid: Union[None, str]
    scope_name: Union[None, str]
    is_profile_managed: bool
    profile_uuid: Union[None, str]
    profile_name: Union[None, str]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid = str(self.uuid)

        role_uuid = str(self.role_uuid)

        role_name = self.role_name

        role_content_type: Union[None, str]
        role_content_type = self.role_content_type

        scope_type: Union[None, str]
        scope_type = self.scope_type

        scope_uuid: Union[None, str]
        scope_uuid = self.scope_uuid

        scope_name: Union[None, str]
        scope_name = self.scope_name

        is_profile_managed = self.is_profile_managed

        profile_uuid: Union[None, str]
        profile_uuid = self.profile_uuid

        profile_name: Union[None, str]
        profile_name = self.profile_name

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uuid": uuid,
                "role_uuid": role_uuid,
                "role_name": role_name,
                "role_content_type": role_content_type,
                "scope_type": scope_type,
                "scope_uuid": scope_uuid,
                "scope_name": scope_name,
                "is_profile_managed": is_profile_managed,
                "profile_uuid": profile_uuid,
                "profile_name": profile_name,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        uuid = UUID(d.pop("uuid"))

        role_uuid = UUID(d.pop("role_uuid"))

        role_name = d.pop("role_name")

        def _parse_role_content_type(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        role_content_type = _parse_role_content_type(d.pop("role_content_type"))

        def _parse_scope_type(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        scope_type = _parse_scope_type(d.pop("scope_type"))

        def _parse_scope_uuid(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        scope_uuid = _parse_scope_uuid(d.pop("scope_uuid"))

        def _parse_scope_name(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        scope_name = _parse_scope_name(d.pop("scope_name"))

        is_profile_managed = d.pop("is_profile_managed")

        def _parse_profile_uuid(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        profile_uuid = _parse_profile_uuid(d.pop("profile_uuid"))

        def _parse_profile_name(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        profile_name = _parse_profile_name(d.pop("profile_name"))

        role_availability_details = cls(
            uuid=uuid,
            role_uuid=role_uuid,
            role_name=role_name,
            role_content_type=role_content_type,
            scope_type=scope_type,
            scope_uuid=scope_uuid,
            scope_name=scope_name,
            is_profile_managed=is_profile_managed,
            profile_uuid=profile_uuid,
            profile_name=profile_name,
        )

        role_availability_details.additional_properties = d
        return role_availability_details

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
