from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.project_posix_group_kind_enum import ProjectPosixGroupKindEnum

T = TypeVar("T", bound="ProjectPosixGroup")


@_attrs_define
class ProjectPosixGroup:
    """
    Attributes:
        kind (ProjectPosixGroupKindEnum):
        gid (int):
        offering_uuid (str):
        offering_name (str):
        provider_name (str):
        role (Union[None, str]):
        scope_type (Union[None, str]):
        scope_name (Union[None, str]):
        scope_uuid (Union[None, str]):
    """

    kind: ProjectPosixGroupKindEnum
    gid: int
    offering_uuid: str
    offering_name: str
    provider_name: str
    role: Union[None, str]
    scope_type: Union[None, str]
    scope_name: Union[None, str]
    scope_uuid: Union[None, str]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        kind = self.kind.value

        gid = self.gid

        offering_uuid = self.offering_uuid

        offering_name = self.offering_name

        provider_name = self.provider_name

        role: Union[None, str]
        role = self.role

        scope_type: Union[None, str]
        scope_type = self.scope_type

        scope_name: Union[None, str]
        scope_name = self.scope_name

        scope_uuid: Union[None, str]
        scope_uuid = self.scope_uuid

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "kind": kind,
                "gid": gid,
                "offering_uuid": offering_uuid,
                "offering_name": offering_name,
                "provider_name": provider_name,
                "role": role,
                "scope_type": scope_type,
                "scope_name": scope_name,
                "scope_uuid": scope_uuid,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        kind = ProjectPosixGroupKindEnum(d.pop("kind"))

        gid = d.pop("gid")

        offering_uuid = d.pop("offering_uuid")

        offering_name = d.pop("offering_name")

        provider_name = d.pop("provider_name")

        def _parse_role(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        role = _parse_role(d.pop("role"))

        def _parse_scope_type(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        scope_type = _parse_scope_type(d.pop("scope_type"))

        def _parse_scope_name(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        scope_name = _parse_scope_name(d.pop("scope_name"))

        def _parse_scope_uuid(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        scope_uuid = _parse_scope_uuid(d.pop("scope_uuid"))

        project_posix_group = cls(
            kind=kind,
            gid=gid,
            offering_uuid=offering_uuid,
            offering_name=offering_name,
            provider_name=provider_name,
            role=role,
            scope_type=scope_type,
            scope_name=scope_name,
            scope_uuid=scope_uuid,
        )

        project_posix_group.additional_properties = d
        return project_posix_group

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
