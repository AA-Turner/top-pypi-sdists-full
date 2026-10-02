from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="ManagedAgentsSessionResourceRef")



@_attrs_define
class ManagedAgentsSessionResourceRef:
    """ A file an automation mounts into every run's sandbox.

        Example:
            {'file_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'mount_path': 'example'}

        Attributes:
            file_id (str): File to mount.
            mount_path (str | Unset): Absolute path inside the sandbox. Omit for the platform default.
     """

    file_id: str
    mount_path: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        file_id = self.file_id

        mount_path = self.mount_path


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "file_id": file_id,
        })
        if mount_path is not UNSET:
            field_dict["mount_path"] = mount_path

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        file_id = d.pop("file_id")

        mount_path = d.pop("mount_path", UNSET)

        managed_agents_session_resource_ref = cls(
            file_id=file_id,
            mount_path=mount_path,
        )


        managed_agents_session_resource_ref.additional_properties = d
        return managed_agents_session_resource_ref

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
