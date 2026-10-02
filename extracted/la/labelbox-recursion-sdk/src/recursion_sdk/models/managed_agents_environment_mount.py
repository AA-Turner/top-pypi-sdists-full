from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="ManagedAgentsEnvironmentMount")



@_attrs_define
class ManagedAgentsEnvironmentMount:
    """ One file or object staged into the sandbox workspace when it is created. Use mounts to give an agent input data it
    should find already on disk at the first turn.

        Example:
            {'mount_path': 'example', 'source': 'example'}

        Attributes:
            mount_path (str | Unset): Absolute path inside the sandbox workspace where the source is placed.
            source (str | Unset): Object or file to stage, as a URI the service can read, e.g. gs://bucket/path.
     """

    mount_path: str | Unset = UNSET
    source: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        mount_path = self.mount_path

        source = self.source


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if mount_path is not UNSET:
            field_dict["mount_path"] = mount_path
        if source is not UNSET:
            field_dict["source"] = source

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        mount_path = d.pop("mount_path", UNSET)

        source = d.pop("source", UNSET)

        managed_agents_environment_mount = cls(
            mount_path=mount_path,
            source=source,
        )


        managed_agents_environment_mount.additional_properties = d
        return managed_agents_environment_mount

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
