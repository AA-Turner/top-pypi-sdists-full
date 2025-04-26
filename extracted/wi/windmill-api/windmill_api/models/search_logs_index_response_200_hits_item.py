from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="SearchLogsIndexResponse200HitsItem")


@_attrs_define
class SearchLogsIndexResponse200HitsItem:
    """
    Attributes:
        dancer (Union[Unset, str]):
    """

    dancer: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        dancer = self.dancer

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if dancer is not UNSET:
            field_dict["dancer"] = dancer

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        dancer = d.pop("dancer", UNSET)

        search_logs_index_response_200_hits_item = cls(
            dancer=dancer,
        )

        search_logs_index_response_200_hits_item.additional_properties = d
        return search_logs_index_response_200_hits_item

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
