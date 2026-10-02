from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.schema_0_type import Schema0Type
from typing import cast

if TYPE_CHECKING:
  from ..models.grading_config_composition_child import GradingConfigCompositionChild





T = TypeVar("T", bound="Schema0")



@_attrs_define
class Schema0:
    """ Composition group that aggregates child scores as a weighted sum; failed children contribute 0 in the numerator
    while their weight remains in the denominator.

        Attributes:
            type_ (Schema0Type): Discriminator: aggregate children as a weighted sum of their scores.
            children (list[GradingConfigCompositionChild]): Child grading configs and weights (1–10 entries); weights
                produce a weighted average.
     """

    type_: Schema0Type
    children: list[GradingConfigCompositionChild]





    def to_dict(self) -> dict[str, Any]:
        from ..models.grading_config_composition_child import GradingConfigCompositionChild # noqa: PLC0415
        type_ = self.type_.value

        children = []
        for children_item_data in self.children:
            children_item = children_item_data.to_dict()
            children.append(children_item)




        field_dict: dict[str, Any] = {}

        field_dict.update({
            "type": type_,
            "children": children,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.grading_config_composition_child import GradingConfigCompositionChild # noqa: PLC0415
        d = dict(src_dict)
        type_ = Schema0Type(d.pop("type"))




        children = []
        _children = d.pop("children")
        for children_item_data in (_children):
            children_item = GradingConfigCompositionChild.from_dict(children_item_data)



            children.append(children_item)


        schema_0 = cls(
            type_=type_,
            children=children,
        )

        return schema_0

