from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.create_tuning_run_dto_properties_cadence_steps_type import CreateTuningRunDtoPropertiesCadenceStepsType
from typing import cast






T = TypeVar("T", bound="CreateTuningRunDtoPropertiesCadenceSteps")



@_attrs_define
class CreateTuningRunDtoPropertiesCadenceSteps:
    """ Evaluate exactly these announced checkpoint steps.

        Attributes:
            type_ (CreateTuningRunDtoPropertiesCadenceStepsType): Cadence variant discriminant.
            steps (list[int]): Exact announced checkpoint steps to evaluate.
     """

    type_: CreateTuningRunDtoPropertiesCadenceStepsType
    steps: list[int]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        type_ = self.type_.value

        steps = self.steps




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "type": type_,
            "steps": steps,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        type_ = CreateTuningRunDtoPropertiesCadenceStepsType(d.pop("type"))




        steps = cast(list[int], d.pop("steps"))


        create_tuning_run_dto_properties_cadence_steps = cls(
            type_=type_,
            steps=steps,
        )


        create_tuning_run_dto_properties_cadence_steps.additional_properties = d
        return create_tuning_run_dto_properties_cadence_steps

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
