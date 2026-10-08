from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

T = TypeVar("T", bound="ConfigurationResponse")


@_attrs_define
class ConfigurationResponse:
    """
    Attributes:
        content_hash (str): The hash of the file of the uploaded tarball
        created_at (datetime.datetime): datetime with the constraint that the value must have timezone info
        created_by (UUID): The ID of the identity who created the entity
        file_count (int): The number of files in the uploaded tarball
        id (UUID): The unique ID of the entity
        profiles (list[str]): The profiles found in the configuration files
        size_bytes (int): The size of the uploaded tarball in bytes
        updated_at (datetime.datetime): datetime with the constraint that the value must have timezone info
        version (int): The version of the deployment. Will increment for each new version of the entity
        workspace_id (UUID): The ID of the workspace the entity belongs to
    """

    content_hash: str
    created_at: datetime.datetime
    created_by: UUID
    file_count: int
    id: UUID
    profiles: list[str]
    size_bytes: int
    updated_at: datetime.datetime
    version: int
    workspace_id: UUID
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        content_hash = self.content_hash

        created_at = self.created_at.isoformat()

        created_by = str(self.created_by)

        file_count = self.file_count

        id = str(self.id)

        profiles = self.profiles

        size_bytes = self.size_bytes

        updated_at = self.updated_at.isoformat()

        version = self.version

        workspace_id = str(self.workspace_id)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "content_hash": content_hash,
                "created_at": created_at,
                "created_by": created_by,
                "file_count": file_count,
                "id": id,
                "profiles": profiles,
                "size_bytes": size_bytes,
                "updated_at": updated_at,
                "version": version,
                "workspace_id": workspace_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        content_hash = d.pop("content_hash")

        created_at = isoparse(d.pop("created_at"))

        created_by = UUID(d.pop("created_by"))

        file_count = d.pop("file_count")

        id = UUID(d.pop("id"))

        profiles = cast(list[str], d.pop("profiles"))

        size_bytes = d.pop("size_bytes")

        updated_at = isoparse(d.pop("updated_at"))

        version = d.pop("version")

        workspace_id = UUID(d.pop("workspace_id"))

        configuration_response = cls(
            content_hash=content_hash,
            created_at=created_at,
            created_by=created_by,
            file_count=file_count,
            id=id,
            profiles=profiles,
            size_bytes=size_bytes,
            updated_at=updated_at,
            version=version,
            workspace_id=workspace_id,
        )

        configuration_response.additional_properties = d
        return configuration_response

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
