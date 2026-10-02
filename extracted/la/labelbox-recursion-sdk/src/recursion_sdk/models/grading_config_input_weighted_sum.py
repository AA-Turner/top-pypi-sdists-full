from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.grading_config_input_weighted_sum_type import GradingConfigInputWeightedSumType
from typing import cast

if TYPE_CHECKING:
  from ..models.grading_config_input_composition_child import GradingConfigInputCompositionChild





T = TypeVar("T", bound="GradingConfigInputWeightedSum")



@_attrs_define
class GradingConfigInputWeightedSum:
    """ Composition group that aggregates child scores as a weighted sum; failed children contribute 0 in the numerator
    while their weight remains in the denominator.

        Attributes:
            type_ (GradingConfigInputWeightedSumType): Discriminator: aggregate children as a weighted sum of their scores.
            children (list[GradingConfigInputCompositionChild]): Child grading configs and weights (1–10 entries); weights
                produce a weighted average.
     """

    type_: GradingConfigInputWeightedSumType
    children: list[GradingConfigInputCompositionChild]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.grading_config_input_composition_child import GradingConfigInputCompositionChild # noqa: PLC0415
        type_ = self.type_.value

        children = []
        for children_item_data in self.children:
            children_item = children_item_data.to_dict()
            children.append(children_item)




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "type": type_,
            "children": children,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.grading_config_input_composition_child import GradingConfigInputCompositionChild # noqa: PLC0415
        d = dict(src_dict)
        type_ = GradingConfigInputWeightedSumType(d.pop("type"))




        children = []
        _children = d.pop("children")
        for children_item_data in (_children):
            children_item = GradingConfigInputCompositionChild.from_dict(children_item_data)



            children.append(children_item)


        grading_config_input_weighted_sum = cls(
            type_=type_,
            children=children,
        )


        grading_config_input_weighted_sum.additional_properties = d
        return grading_config_input_weighted_sum

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
