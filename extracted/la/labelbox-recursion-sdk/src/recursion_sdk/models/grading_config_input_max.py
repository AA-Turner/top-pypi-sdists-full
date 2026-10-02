from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.grading_config_input_max_type import GradingConfigInputMaxType
from typing import cast

if TYPE_CHECKING:
  from ..models.grading_config_input_composition_child import GradingConfigInputCompositionChild





T = TypeVar("T", bound="GradingConfigInputMax")



@_attrs_define
class GradingConfigInputMax:
    """ Composition group that returns the maximum score among its children; failed children are skipped.

        Attributes:
            type_ (GradingConfigInputMaxType): Discriminator: aggregate children by selecting the highest child score.
            children (list[GradingConfigInputCompositionChild]): Child grading configs (1–10 entries); child weights are
                ignored for max selection.
     """

    type_: GradingConfigInputMaxType
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
        type_ = GradingConfigInputMaxType(d.pop("type"))




        children = []
        _children = d.pop("children")
        for children_item_data in (_children):
            children_item = GradingConfigInputCompositionChild.from_dict(children_item_data)



            children.append(children_item)


        grading_config_input_max = cls(
            type_=type_,
            children=children,
        )


        grading_config_input_max.additional_properties = d
        return grading_config_input_max

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
