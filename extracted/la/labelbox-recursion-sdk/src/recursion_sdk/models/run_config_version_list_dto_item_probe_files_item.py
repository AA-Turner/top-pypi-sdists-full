from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="RunConfigVersionListDtoItemProbeFilesItem")



@_attrs_define
class RunConfigVersionListDtoItemProbeFilesItem:
    """ Workspace file supplied by the probe in addition to any mounts from the run-config payload.

        Attributes:
            object_path (str): GCS object path the agent-service FilesService reads when staging the probe.
            mount_path (str): Absolute container path where the probe file is mounted at probe-run time.
     """

    object_path: str
    mount_path: str





    def to_dict(self) -> dict[str, Any]:
        object_path = self.object_path

        mount_path = self.mount_path


        field_dict: dict[str, Any] = {}

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

        run_config_version_list_dto_item_probe_files_item = cls(
            object_path=object_path,
            mount_path=mount_path,
        )

        return run_config_version_list_dto_item_probe_files_item

