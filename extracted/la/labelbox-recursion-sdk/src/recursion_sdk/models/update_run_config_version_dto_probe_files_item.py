from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="UpdateRunConfigVersionDtoProbeFilesItem")



@_attrs_define
class UpdateRunConfigVersionDtoProbeFilesItem:
    """ Workspace file supplied by the probe in addition to any mounts from the run-config payload.

        Attributes:
            object_path (str): GCS object path the agent-service FilesService reads when staging the probe.
            mount_path (str): Absolute container path where the probe file is mounted at probe-run time.
     """

    object_path: str
    mount_path: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        object_path = self.object_path

        mount_path = self.mount_path


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "objectPath": object_path,
            "mountPath": mount_path,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        object_path = d.pop("objectPath")

        mount_path = d.pop("mountPath")

        update_run_config_version_dto_probe_files_item = cls(
            object_path=object_path,
            mount_path=mount_path,
        )


        update_run_config_version_dto_probe_files_item.additional_properties = d
        return update_run_config_version_dto_probe_files_item

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
