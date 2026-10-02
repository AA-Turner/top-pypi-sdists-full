from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.create_compute_request_dto_accelerator_name import CreateComputeRequestDtoAcceleratorName
from ..models.create_compute_request_dto_accelerator_type import CreateComputeRequestDtoAcceleratorType






T = TypeVar("T", bound="CreateComputeRequestDtoAccelerator")



@_attrs_define
class CreateComputeRequestDtoAccelerator:
    """ Optional GPU accelerator to attach to the compute.

        Attributes:
            type_ (CreateComputeRequestDtoAcceleratorType): Accelerator kind; only "gpu" is currently supported.
            name (CreateComputeRequestDtoAcceleratorName): GPU model identifier (e.g. "nvidia-l4", "nvidia-a100").
     """

    type_: CreateComputeRequestDtoAcceleratorType
    name: CreateComputeRequestDtoAcceleratorName
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        type_ = self.type_.value

        name = self.name.value


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "type": type_,
            "name": name,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        type_ = CreateComputeRequestDtoAcceleratorType(d.pop("type"))




        name = CreateComputeRequestDtoAcceleratorName(d.pop("name"))




        create_compute_request_dto_accelerator = cls(
            type_=type_,
            name=name,
        )


        create_compute_request_dto_accelerator.additional_properties = d
        return create_compute_request_dto_accelerator

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
