from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.grading_config_none_type import GradingConfigNoneType






T = TypeVar("T", bound="GradingConfigNone")



@_attrs_define
class GradingConfigNone:
    """ Grading config leaf indicating no grading should run; produces no score.

        Attributes:
            type_ (GradingConfigNoneType): Discriminator: no grading is performed for this node.
     """

    type_: GradingConfigNoneType





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
        type_ = GradingConfigNoneType(d.pop("type"))




        grading_config_none = cls(
            type_=type_,
        )

        return grading_config_none

