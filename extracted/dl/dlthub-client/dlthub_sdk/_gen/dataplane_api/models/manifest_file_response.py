from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ManifestFileResponse")


@_attrs_define
class ManifestFileResponse:
    """
    Attributes:
        relative_path (str): Path of the file inside the package.
        sha3_256 (str): Digest of the contents, or of `linkname` for a symlink.
        size_bytes (int): Size of the file.
        linkname (None | str | Unset): Symlink target; set for symlink entries only.
    """

    relative_path: str
    sha3_256: str
    size_bytes: int
    linkname: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        relative_path = self.relative_path

        sha3_256 = self.sha3_256

        size_bytes = self.size_bytes

        linkname: None | str | Unset
        if isinstance(self.linkname, Unset):
            linkname = UNSET
        else:
            linkname = self.linkname

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "relative_path": relative_path,
                "sha3_256": sha3_256,
                "size_bytes": size_bytes,
            }
        )
        if linkname is not UNSET:
            field_dict["linkname"] = linkname

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        relative_path = d.pop("relative_path")

        sha3_256 = d.pop("sha3_256")

        size_bytes = d.pop("size_bytes")

        def _parse_linkname(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        linkname = _parse_linkname(d.pop("linkname", UNSET))

        manifest_file_response = cls(
            relative_path=relative_path,
            sha3_256=sha3_256,
            size_bytes=size_bytes,
            linkname=linkname,
        )

        manifest_file_response.additional_properties = d
        return manifest_file_response

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
