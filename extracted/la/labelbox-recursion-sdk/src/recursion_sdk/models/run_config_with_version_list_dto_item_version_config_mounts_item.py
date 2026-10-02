from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="RunConfigWithVersionListDtoItemVersionConfigMountsItem")



@_attrs_define
class RunConfigWithVersionListDtoItemVersionConfigMountsItem:
    """ External file mount that references a previously uploaded GCS object by file ID.

        Attributes:
            source (str): Platform file ID referencing an object already uploaded to GCS.
            mount_path (str): Absolute container path where the referenced file is mounted at compute creation time. Must be
                absolute and must not contain parent-directory segments.
     """

    source: str
    mount_path: str





    def to_dict(self) -> dict[str, Any]:
        source = self.source

        mount_path = self.mount_path


        field_dict: dict[str, Any] = {}

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

        run_config_with_version_list_dto_item_version_config_mounts_item = cls(
            source=source,
            mount_path=mount_path,
        )

        return run_config_with_version_list_dto_item_version_config_mounts_item

