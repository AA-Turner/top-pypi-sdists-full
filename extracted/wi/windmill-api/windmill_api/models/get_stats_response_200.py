from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="GetStatsResponse200")


@_attrs_define
class GetStatsResponse200:
    """
    Attributes:
        signature (Union[Unset, str]):
        data (Union[Unset, str]):
    """

    signature: Union[Unset, str] = UNSET
    data: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        signature = self.signature
        data = self.data

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if signature is not UNSET:
            field_dict["signature"] = signature
        if data is not UNSET:
            field_dict["data"] = data

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        signature = d.pop("signature", UNSET)

        data = d.pop("data", UNSET)

        get_stats_response_200 = cls(
            signature=signature,
            data=data,
        )

        get_stats_response_200.additional_properties = d
        return get_stats_response_200

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
