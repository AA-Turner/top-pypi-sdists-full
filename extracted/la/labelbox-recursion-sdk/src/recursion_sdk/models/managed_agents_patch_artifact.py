from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="ManagedAgentsPatchArtifact")



@_attrs_define
class ManagedAgentsPatchArtifact:
    """ Metadata for the working-tree patch captured from a repository automation. Only the digest and size are recorded on
    the result; the patch body itself is a transcript artifact event addressed by event_id.

        Example:
            {'byte_size': 1, 'changed': True, 'event_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'patch_sha256': 'example'}

        Attributes:
            byte_size (int): Size of the captured patch in bytes. Capture fails above 4 MiB.
            changed (bool): Whether the patch is non-empty, that is, whether the agent left any working-tree change at all.
            patch_sha256 (str): SHA-256 of the captured patch bytes, as lowercase hex. Empty when no patch was captured.
            event_id (str | Unset): Transcript event id (UUID) of the artifact event carrying the patch body, readable
                through listSessionEvents. Absent when no patch was captured.
     """

    byte_size: int
    changed: bool
    patch_sha256: str
    event_id: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        byte_size = self.byte_size

        changed = self.changed

        patch_sha256 = self.patch_sha256

        event_id = self.event_id


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "byte_size": byte_size,
            "changed": changed,
            "patch_sha256": patch_sha256,
        })
        if event_id is not UNSET:
            field_dict["event_id"] = event_id

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        byte_size = d.pop("byte_size")

        changed = d.pop("changed")

        patch_sha256 = d.pop("patch_sha256")

        event_id = d.pop("event_id", UNSET)

        managed_agents_patch_artifact = cls(
            byte_size=byte_size,
            changed=changed,
            patch_sha256=patch_sha256,
            event_id=event_id,
        )


        managed_agents_patch_artifact.additional_properties = d
        return managed_agents_patch_artifact

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
