import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="FreeipaProfileRequest")


@_attrs_define
class FreeipaProfileRequest:
    """
    Attributes:
        username (str): Letters, numbers and ./+/-/_ characters
        agreement_date (Union[Unset, datetime.datetime]): Indicates when the user has agreed with the policy.
    """

    username: str
    agreement_date: Union[Unset, datetime.datetime] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        username = self.username

        agreement_date: Union[Unset, str] = UNSET
        if not isinstance(self.agreement_date, Unset):
            agreement_date = self.agreement_date.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "username": username,
            }
        )
        if agreement_date is not UNSET:
            field_dict["agreement_date"] = agreement_date

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        username = d.pop("username")

        _agreement_date = d.pop("agreement_date", UNSET)
        agreement_date: Union[Unset, datetime.datetime]
        if isinstance(_agreement_date, Unset):
            agreement_date = UNSET
        else:
            agreement_date = isoparse(_agreement_date)

        freeipa_profile_request = cls(
            username=username,
            agreement_date=agreement_date,
        )

        freeipa_profile_request.additional_properties = d
        return freeipa_profile_request

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
