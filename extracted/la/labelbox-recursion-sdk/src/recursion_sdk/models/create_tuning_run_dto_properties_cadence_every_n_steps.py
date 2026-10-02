from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.create_tuning_run_dto_properties_cadence_every_n_steps_type import CreateTuningRunDtoPropertiesCadenceEveryNStepsType






T = TypeVar("T", bound="CreateTuningRunDtoPropertiesCadenceEveryNSteps")



@_attrs_define
class CreateTuningRunDtoPropertiesCadenceEveryNSteps:
    """ Evaluate every Nth announced checkpoint step.

        Attributes:
            type_ (CreateTuningRunDtoPropertiesCadenceEveryNStepsType): Cadence variant discriminant.
            n (int): Evaluate every Nth announced checkpoint step.
     """

    type_: CreateTuningRunDtoPropertiesCadenceEveryNStepsType
    n: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        type_ = self.type_.value

        n = self.n


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "type": type_,
            "n": n,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        type_ = CreateTuningRunDtoPropertiesCadenceEveryNStepsType(d.pop("type"))




        n = d.pop("n")

        create_tuning_run_dto_properties_cadence_every_n_steps = cls(
            type_=type_,
            n=n,
        )


        create_tuning_run_dto_properties_cadence_every_n_steps.additional_properties = d
        return create_tuning_run_dto_properties_cadence_every_n_steps

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
