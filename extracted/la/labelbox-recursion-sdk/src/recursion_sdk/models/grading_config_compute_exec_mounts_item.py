from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from uuid import UUID






T = TypeVar("T", bound="GradingConfigComputeExecMountsItem")



@_attrs_define
class GradingConfigComputeExecMountsItem:
    """ A file copied into the persistent compute for a compute_exec grade.

        Attributes:
            file_id (UUID): Identifier of the already-uploaded platform file to mount.
            mount_path (str): Absolute container path the file is copied to on the compute before grading; must live under
                the run config's computeEnv.sharedMountDir (default /workspace/files) and outside the reserved
                /workspace/files/problem/ subtree.
     """

    file_id: UUID
    mount_path: str





    def to_dict(self) -> dict[str, Any]:
        file_id = str(self.file_id)

        mount_path = self.mount_path


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "fileId": file_id,
            "mountPath": mount_path,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        file_id = UUID(d.pop("fileId"))




        mount_path = d.pop("mountPath")

        grading_config_compute_exec_mounts_item = cls(
            file_id=file_id,
            mount_path=mount_path,
        )

        return grading_config_compute_exec_mounts_item

