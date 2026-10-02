from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="ManagedAgentsSkillBundleEntry")



@_attrs_define
class ManagedAgentsSkillBundleEntry:
    """ One file inside a skill version's bundle, listed so a caller can see what a version ships, and what of it the
    sandbox will be able to run, without downloading the archive.

        Example:
            {'bytes': 1, 'mode': 1, 'path': 'example', 'sha256': 'example'}

        Attributes:
            bytes_ (int): Size of the file in bytes.
            mode (int): Permission bits the file is extracted with: 0755 for files under scripts/, 0644 otherwise. Assigned
                by this platform from the file's location, never taken from the uploaded archive.
            path (str): Path of the file relative to the skill's own directory, e.g. scripts/tag.sh.
            sha256 (str): SHA-256 of the file's contents. Stable across repacking, so comparing two versions' entries
                decides which files were added, removed, or changed without downloading either bundle.
     """

    bytes_: int
    mode: int
    path: str
    sha256: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        bytes_ = self.bytes_

        mode = self.mode

        path = self.path

        sha256 = self.sha256


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "bytes": bytes_,
            "mode": mode,
            "path": path,
            "sha256": sha256,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        bytes_ = d.pop("bytes")

        mode = d.pop("mode")

        path = d.pop("path")

        sha256 = d.pop("sha256")

        managed_agents_skill_bundle_entry = cls(
            bytes_=bytes_,
            mode=mode,
            path=path,
            sha256=sha256,
        )


        managed_agents_skill_bundle_entry.additional_properties = d
        return managed_agents_skill_bundle_entry

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
