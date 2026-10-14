from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="ComponentFormulaTarget")


@_attrs_define
class ComponentFormulaTarget:
    """
    Attributes:
        component_type (str):
        formula (str): Expression over input, numbers, + - * / and parentheses, for example input * 2 * 0.25.
    """

    component_type: str
    formula: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        component_type = self.component_type

        formula = self.formula

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "component_type": component_type,
                "formula": formula,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        component_type = d.pop("component_type")

        formula = d.pop("formula")

        component_formula_target = cls(
            component_type=component_type,
            formula=formula,
        )

        component_formula_target.additional_properties = d
        return component_formula_target

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
