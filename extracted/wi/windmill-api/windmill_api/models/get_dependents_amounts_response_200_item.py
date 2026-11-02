from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="GetDependentsAmountsResponse200Item")


@_attrs_define
class GetDependentsAmountsResponse200Item:
    """
    Attributes:
        imported_path (str):
        count (int):
    """

    imported_path: str
    count: int
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        imported_path = self.imported_path
        count = self.count

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "imported_path": imported_path,
                "count": count,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        imported_path = d.pop("imported_path")

        count = d.pop("count")

        get_dependents_amounts_response_200_item = cls(
            imported_path=imported_path,
            count=count,
        )

        get_dependents_amounts_response_200_item.additional_properties = d
        return get_dependents_amounts_response_200_item

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
