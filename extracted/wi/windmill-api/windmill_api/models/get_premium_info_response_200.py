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
        is_past_due (bool):
        usage (Union[Unset, float]):
        status (Union[Unset, str]):
        max_tolerated_executions (Union[Unset, float]):
    """

    premium: bool
    owner: str
    is_past_due: bool
    usage: Union[Unset, float] = UNSET
    status: Union[Unset, str] = UNSET
    max_tolerated_executions: Union[Unset, float] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        premium = self.premium
        owner = self.owner
        is_past_due = self.is_past_due
        usage = self.usage
        status = self.status
        max_tolerated_executions = self.max_tolerated_executions

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "premium": premium,
                "owner": owner,
                "is_past_due": is_past_due,
            }
        )
        if usage is not UNSET:
            field_dict["usage"] = usage
        if status is not UNSET:
            field_dict["status"] = status
        if max_tolerated_executions is not UNSET:
            field_dict["max_tolerated_executions"] = max_tolerated_executions

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        premium = d.pop("premium")

        owner = d.pop("owner")

        is_past_due = d.pop("is_past_due")

        usage = d.pop("usage", UNSET)

        status = d.pop("status", UNSET)

        max_tolerated_executions = d.pop("max_tolerated_executions", UNSET)

        get_premium_info_response_200 = cls(
            premium=premium,
            owner=owner,
            is_past_due=is_past_due,
            usage=usage,
            status=status,
            max_tolerated_executions=max_tolerated_executions,
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
