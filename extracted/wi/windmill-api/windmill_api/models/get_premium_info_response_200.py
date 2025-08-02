from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="GetPremiumInfoResponse200")


@_attrs_define
class GetPremiumInfoResponse200:
    """
    Attributes:
        premium (bool):
        owner (str):
        usage (Union[Unset, float]):
        status (Union[Unset, str]):
    """

    premium: bool
    owner: str
    usage: Union[Unset, float] = UNSET
    status: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        premium = self.premium
        owner = self.owner
        usage = self.usage
        status = self.status

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "premium": premium,
                "owner": owner,
            }
        )
        if usage is not UNSET:
            field_dict["usage"] = usage
        if status is not UNSET:
            field_dict["status"] = status

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        premium = d.pop("premium")

        owner = d.pop("owner")

        usage = d.pop("usage", UNSET)

        status = d.pop("status", UNSET)

        get_premium_info_response_200 = cls(
            premium=premium,
            owner=owner,
            usage=usage,
            status=status,
        )

        get_premium_info_response_200.additional_properties = d
        return get_premium_info_response_200

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
