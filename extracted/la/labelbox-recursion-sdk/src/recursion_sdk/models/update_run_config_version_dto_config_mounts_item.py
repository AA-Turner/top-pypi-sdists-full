from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="UpdateRunConfigVersionDtoConfigMountsItem")



@_attrs_define
class UpdateRunConfigVersionDtoConfigMountsItem:
    """ External file mount that references a previously uploaded GCS object by file ID.

        Attributes:
            source (str): Platform file ID referencing an object already uploaded to GCS.
            mount_path (str): Absolute container path where the referenced file is mounted at compute creation time. Must be
                absolute and must not contain parent-directory segments.
     """

    source: str
    mount_path: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        source = self.source

        mount_path = self.mount_path


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "source": source,
            "mountPath": mount_path,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        source = d.pop("source")

        mount_path = d.pop("mountPath")

        update_run_config_version_dto_config_mounts_item = cls(
            source=source,
            mount_path=mount_path,
        )


        update_run_config_version_dto_config_mounts_item.additional_properties = d
        return update_run_config_version_dto_config_mounts_item

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
