from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.grading_config_input_rubric_type import GradingConfigInputRubricType






T = TypeVar("T", bound="GradingConfigInputRubric")



@_attrs_define
class GradingConfigInputRubric:
    """ Grading config leaf that scores the run against the problem’s structured rubric.

        Attributes:
            type_ (GradingConfigInputRubricType): Discriminator: grade by scoring against the problem’s rubric.
     """

    type_: GradingConfigInputRubricType
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        type_ = self.type_.value


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "type": type_,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        type_ = GradingConfigInputRubricType(d.pop("type"))




        grading_config_input_rubric = cls(
            type_=type_,
        )


        grading_config_input_rubric.additional_properties = d
        return grading_config_input_rubric

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
