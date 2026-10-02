from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.qa_config_response_array_dto_item_accelerator_type_0_type import QaConfigResponseArrayDtoItemAcceleratorType0Type
from ..types import UNSET, Unset






T = TypeVar("T", bound="QaConfigResponseArrayDtoItemAcceleratorType0")



@_attrs_define
class QaConfigResponseArrayDtoItemAcceleratorType0:
    """ Hardware accelerator configuration requested for a QA job container.

        Attributes:
            type_ (QaConfigResponseArrayDtoItemAcceleratorType0Type): Hardware accelerator family: graphics processor or
                tensor processor.
            name (str): Accelerator model name as recognized by the launcher.
            count (int | Unset): Number of accelerators to attach to the job container; defaults to 1 when unset.
     """

    type_: QaConfigResponseArrayDtoItemAcceleratorType0Type
    name: str
    count: int | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        type_ = self.type_.value

        name = self.name

        count = self.count


        field_dict: dict[str, Any] = {}

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
        type_ = QaConfigResponseArrayDtoItemAcceleratorType0Type(d.pop("type"))




        name = d.pop("name")

        count = d.pop("count", UNSET)

        qa_config_response_array_dto_item_accelerator_type_0 = cls(
            type_=type_,
            name=name,
            count=count,
        )

        return qa_config_response_array_dto_item_accelerator_type_0

