from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.update_qa_config_body_dto_accelerator_type_0_type import UpdateQaConfigBodyDtoAcceleratorType0Type
from ..types import UNSET, Unset






T = TypeVar("T", bound="UpdateQaConfigBodyDtoAcceleratorType0")



@_attrs_define
class UpdateQaConfigBodyDtoAcceleratorType0:
    """ Hardware accelerator configuration requested for a QA job container.

        Attributes:
            type_ (UpdateQaConfigBodyDtoAcceleratorType0Type): Hardware accelerator family: graphics processor or tensor
                processor.
            name (str): Accelerator model name as recognized by the launcher.
            count (int | Unset): Number of accelerators to attach to the job container; defaults to 1 when unset.
     """

    type_: UpdateQaConfigBodyDtoAcceleratorType0Type
    name: str
    count: int | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        type_ = self.type_.value

        name = self.name

        count = self.count


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "type": type_,
            "name": name,
        })
        if count is not UNSET:
            field_dict["count"] = count

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        type_ = UpdateQaConfigBodyDtoAcceleratorType0Type(d.pop("type"))




        name = d.pop("name")

        count = d.pop("count", UNSET)

        update_qa_config_body_dto_accelerator_type_0 = cls(
            type_=type_,
            name=name,
            count=count,
        )


        update_qa_config_body_dto_accelerator_type_0.additional_properties = d
        return update_qa_config_body_dto_accelerator_type_0

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
