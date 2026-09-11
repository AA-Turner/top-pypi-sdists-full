from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="ConfigurationCreatePayload")


@_attrs_define
class ConfigurationCreatePayload:
    """
    Attributes:
        content_hash (str): sha3-256 over the configuration manifest
        created_by (UUID): Identity id (from token sub)
        file_count (int): Number of files in the tarball
        id (UUID): Pre-allocated configuration id (from upload token)
        profiles (list[str]): Profile names extracted from the manifest's `.dlt/*.toml` paths
        size (int): Tarball size in bytes
    """

    content_hash: str
    created_by: UUID
    file_count: int
    id: UUID
    profiles: list[str]
    size: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        content_hash = self.content_hash

        created_by = str(self.created_by)

        file_count = self.file_count

        id = str(self.id)

        profiles = self.profiles

        size = self.size

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "content_hash": content_hash,
                "created_by": created_by,
                "file_count": file_count,
                "id": id,
                "profiles": profiles,
                "size": size,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        content_hash = d.pop("content_hash")

        created_by = UUID(d.pop("created_by"))

        file_count = d.pop("file_count")

        id = UUID(d.pop("id"))

        profiles = cast(list[str], d.pop("profiles"))

        size = d.pop("size")

        configuration_create_payload = cls(
            content_hash=content_hash,
            created_by=created_by,
            file_count=file_count,
            id=id,
            profiles=profiles,
            size=size,
        )

        configuration_create_payload.additional_properties = d
        return configuration_create_payload

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
