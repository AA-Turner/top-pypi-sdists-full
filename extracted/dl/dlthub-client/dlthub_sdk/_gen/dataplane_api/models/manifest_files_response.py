from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.manifest_file_response import ManifestFileResponse


T = TypeVar("T", bound="ManifestFilesResponse")


@_attrs_define
class ManifestFilesResponse:
    """
    Attributes:
        engine_version (int): Manifest engine version.
        files (list[ManifestFileResponse]): The files in the package.
    """

    engine_version: int
    files: list[ManifestFileResponse]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        engine_version = self.engine_version

        files = []
        for files_item_data in self.files:
            files_item = files_item_data.to_dict()
            files.append(files_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "engine_version": engine_version,
                "files": files,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.manifest_file_response import ManifestFileResponse

        d = dict(src_dict)
        engine_version = d.pop("engine_version")

        files = []
        _files = d.pop("files")
        for files_item_data in _files:
            files_item = ManifestFileResponse.from_dict(files_item_data)

            files.append(files_item)

        manifest_files_response = cls(
            engine_version=engine_version,
            files=files,
        )

        manifest_files_response.additional_properties = d
        return manifest_files_response

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
