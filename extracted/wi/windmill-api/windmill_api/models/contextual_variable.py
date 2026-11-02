from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="ContextualVariable")


@_attrs_define
class ContextualVariable:
    """
    Attributes:
        name (str):
        value (str):
        description (str):
        is_custom (bool):
    """

    name: str
    value: str
    description: str
    is_custom: bool
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        value = self.value
        description = self.description
        is_custom = self.is_custom

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "value": value,
                "description": description,
                "is_custom": is_custom,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        value = d.pop("value")

        description = d.pop("description")

        is_custom = d.pop("is_custom")

        contextual_variable = cls(
            name=name,
            value=value,
            description=description,
            is_custom=is_custom,
        )

        contextual_variable.additional_properties = d
        return contextual_variable

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
