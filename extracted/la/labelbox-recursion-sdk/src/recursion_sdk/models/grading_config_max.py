from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.grading_config_max_type import GradingConfigMaxType
from typing import cast

if TYPE_CHECKING:
  from ..models.grading_config_composition_child import GradingConfigCompositionChild





T = TypeVar("T", bound="GradingConfigMax")



@_attrs_define
class GradingConfigMax:
    """ Composition group that returns the maximum score among its children; failed children are skipped.

        Attributes:
            type_ (GradingConfigMaxType): Discriminator: aggregate children by selecting the highest child score.
            children (list[GradingConfigCompositionChild]): Child grading configs (1–10 entries); child weights are ignored
                for max selection.
     """

    type_: GradingConfigMaxType
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
        type_ = GradingConfigMaxType(d.pop("type"))




        children = []
        _children = d.pop("children")
        for children_item_data in (_children):
            children_item = GradingConfigCompositionChild.from_dict(children_item_data)



            children.append(children_item)


        grading_config_max = cls(
            type_=type_,
            children=children,
        )

        return grading_config_max

