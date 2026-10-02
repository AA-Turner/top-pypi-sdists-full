from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="UpdateGoldStandardDtoType1")



@_attrs_define
class UpdateGoldStandardDtoType1:
    """ 
        Attributes:
            is_gold_standard (bool): Clears gold-standard status; the file remains attached but is no longer mounted.
     """

    is_gold_standard: bool
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        is_gold_standard = self.is_gold_standard


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "isGoldStandard": is_gold_standard,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        is_gold_standard = d.pop("isGoldStandard")

        update_gold_standard_dto_type_1 = cls(
            is_gold_standard=is_gold_standard,
        )


        update_gold_standard_dto_type_1.additional_properties = d
        return update_gold_standard_dto_type_1

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
