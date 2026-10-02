from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.grading_config_rubric_type import GradingConfigRubricType






T = TypeVar("T", bound="GradingConfigRubric")



@_attrs_define
class GradingConfigRubric:
    """ Grading config leaf that scores the run against the problem’s structured rubric.

        Attributes:
            type_ (GradingConfigRubricType): Discriminator: grade by scoring against the problem’s rubric.
     """

    type_: GradingConfigRubricType





    def to_dict(self) -> dict[str, Any]:
        type_ = self.type_.value


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "type": type_,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        type_ = GradingConfigRubricType(d.pop("type"))




        grading_config_rubric = cls(
            type_=type_,
        )

        return grading_config_rubric

