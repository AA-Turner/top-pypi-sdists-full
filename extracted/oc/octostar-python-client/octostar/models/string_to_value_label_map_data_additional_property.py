from typing import (
    Any,
    Dict,
    Type,
    TypeVar,
    Tuple,
    Optional,
    BinaryIO,
    TextIO,
    TYPE_CHECKING,
)

from typing import List


import attr

from ..types import UNSET, Unset


T = TypeVar("T", bound="StringToValueLabelMapDataAdditionalProperty")


@attr.s(auto_attribs=True)
class StringToValueLabelMapDataAdditionalProperty:
    """
    ### Attributes:
    * `value (float)`: None
    * `label (str)`: None
    """

    value: float
    label: str
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        value = self.value
        label = self.label

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "value": value,
                "label": label,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        value = d.pop("value")

        label = d.pop("label")

        string_to_value_label_map_data_additional_property = cls(
            value=value,
            label=label,
        )

        string_to_value_label_map_data_additional_property.additional_properties = d
        return string_to_value_label_map_data_additional_property

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
