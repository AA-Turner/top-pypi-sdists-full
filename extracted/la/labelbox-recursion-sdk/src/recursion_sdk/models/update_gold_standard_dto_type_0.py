from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="UpdateGoldStandardDtoType0")



@_attrs_define
class UpdateGoldStandardDtoType0:
    """ 
        Attributes:
            is_gold_standard (bool): Marks the file as gold-standard; requires a mount path.
            gold_standard_mount_path (str): Container path the gold-standard file is mounted at. Must live under the
                workspace root and avoid reserved grader-support paths.
     """

    is_gold_standard: bool
    gold_standard_mount_path: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        is_gold_standard = self.is_gold_standard

        gold_standard_mount_path = self.gold_standard_mount_path


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "isGoldStandard": is_gold_standard,
            "goldStandardMountPath": gold_standard_mount_path,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        is_gold_standard = d.pop("isGoldStandard")

        gold_standard_mount_path = d.pop("goldStandardMountPath")

        update_gold_standard_dto_type_0 = cls(
            is_gold_standard=is_gold_standard,
            gold_standard_mount_path=gold_standard_mount_path,
        )


        update_gold_standard_dto_type_0.additional_properties = d
        return update_gold_standard_dto_type_0

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
