import datetime
from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="UpdateTokenLimitsJsonBody")


@_attrs_define
class UpdateTokenLimitsJsonBody:
    """
    Attributes:
        expiration (Union[Unset, None, datetime.datetime]): new expiration (null = never expires)
        allowed_ips (Union[Unset, None, List[str]]): IPs or CIDRs the token may be used from (null = anywhere)
    """

    expiration: Union[Unset, None, datetime.datetime] = UNSET
    allowed_ips: Union[Unset, None, List[str]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        expiration: Union[Unset, None, str] = UNSET
        if not isinstance(self.expiration, Unset):
            expiration = self.expiration.isoformat() if self.expiration else None

        allowed_ips: Union[Unset, None, List[str]] = UNSET
        if not isinstance(self.allowed_ips, Unset):
            if self.allowed_ips is None:
                allowed_ips = None
            else:
                allowed_ips = self.allowed_ips

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if expiration is not UNSET:
            field_dict["expiration"] = expiration
        if allowed_ips is not UNSET:
            field_dict["allowed_ips"] = allowed_ips

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _expiration = d.pop("expiration", UNSET)
        expiration: Union[Unset, None, datetime.datetime]
        if _expiration is None:
            expiration = None
        elif isinstance(_expiration, Unset):
            expiration = UNSET
        else:
            expiration = isoparse(_expiration)

        allowed_ips = cast(List[str], d.pop("allowed_ips", UNSET))

        update_token_limits_json_body = cls(
            expiration=expiration,
            allowed_ips=allowed_ips,
        )

        update_token_limits_json_body.additional_properties = d
        return update_token_limits_json_body

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
