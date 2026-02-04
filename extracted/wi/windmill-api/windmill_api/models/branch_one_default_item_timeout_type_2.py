from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.branch_one_default_item_timeout_type_2_type import BranchOneDefaultItemTimeoutType2Type

T = TypeVar("T", bound="BranchOneDefaultItemTimeoutType2")


@_attrs_define
class BranchOneDefaultItemTimeoutType2:
    """Value resolved by the AI runtime for this input. The AI engine decides how to satisfy the parameter.

    Attributes:
        type (BranchOneDefaultItemTimeoutType2Type):
    """

    type: BranchOneDefaultItemTimeoutType2Type
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        type = self.type.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        type = BranchOneDefaultItemTimeoutType2Type(d.pop("type"))

        branch_one_default_item_timeout_type_2 = cls(
            type=type,
        )

        branch_one_default_item_timeout_type_2.additional_properties = d
        return branch_one_default_item_timeout_type_2

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
