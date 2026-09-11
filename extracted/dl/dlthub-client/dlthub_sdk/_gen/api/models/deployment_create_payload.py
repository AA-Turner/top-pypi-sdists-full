from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="DeploymentCreatePayload")


@_attrs_define
class DeploymentCreatePayload:
    """
    Attributes:
        content_hash (str): sha3-256 over the deployment manifest
        created_by (UUID): Identity id (from token sub)
        file_count (int): Number of files in the tarball
        id (UUID): Pre-allocated deployment id (from upload token)
        requirements_size (int): Size of the requirements manifest blob in bytes
        size (int): Tarball size in bytes
    """

    content_hash: str
    created_by: UUID
    file_count: int
    id: UUID
    requirements_size: int
    size: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        content_hash = self.content_hash

        created_by = str(self.created_by)

        file_count = self.file_count

        id = str(self.id)

        requirements_size = self.requirements_size

        size = self.size

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "content_hash": content_hash,
                "created_by": created_by,
                "file_count": file_count,
                "id": id,
                "requirements_size": requirements_size,
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

        requirements_size = d.pop("requirements_size")

        size = d.pop("size")

        deployment_create_payload = cls(
            content_hash=content_hash,
            created_by=created_by,
            file_count=file_count,
            id=id,
            requirements_size=requirements_size,
            size=size,
        )

        deployment_create_payload.additional_properties = d
        return deployment_create_payload

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
