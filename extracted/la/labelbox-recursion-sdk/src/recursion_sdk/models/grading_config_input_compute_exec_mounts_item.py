from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from uuid import UUID






T = TypeVar("T", bound="GradingConfigInputComputeExecMountsItem")



@_attrs_define
class GradingConfigInputComputeExecMountsItem:
    """ A file copied into the persistent compute for a compute_exec grade.

        Attributes:
            file_id (UUID): Identifier of the already-uploaded platform file to mount.
            mount_path (str): Absolute container path the file is copied to on the compute before grading; must live under
                the run config's computeEnv.sharedMountDir (default /workspace/files) and outside the reserved
                /workspace/files/problem/ subtree.
     """

    file_id: UUID
    mount_path: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        file_id = str(self.file_id)

        mount_path = self.mount_path


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
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

        grading_config_input_compute_exec_mounts_item = cls(
            file_id=file_id,
            mount_path=mount_path,
        )


        grading_config_input_compute_exec_mounts_item.additional_properties = d
        return grading_config_input_compute_exec_mounts_item

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
