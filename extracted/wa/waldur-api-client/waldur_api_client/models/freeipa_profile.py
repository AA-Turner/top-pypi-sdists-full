import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="FreeipaProfile")


@_attrs_define
class FreeipaProfile:
    """
    Attributes:
        uuid (UUID):
        username (str): Letters, numbers and ./+/-/_ characters
        is_active (bool):
        user (str):
        user_uuid (UUID):
        user_username (str): Required. 128 characters or fewer. Lowercase letters, numbers and @/./+/-/_ characters
        user_full_name (str):
        agreement_date (Union[Unset, datetime.datetime]): Indicates when the user has agreed with the policy.
    """

    uuid: UUID
    username: str
    is_active: bool
    user: str
    user_uuid: UUID
    user_username: str
    user_full_name: str
    agreement_date: Union[Unset, datetime.datetime] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid = str(self.uuid)

        username = self.username

        is_active = self.is_active

        user = self.user

        user_uuid = str(self.user_uuid)

        user_username = self.user_username

        user_full_name = self.user_full_name

        agreement_date: Union[Unset, str] = UNSET
        if not isinstance(self.agreement_date, Unset):
            agreement_date = self.agreement_date.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uuid": uuid,
                "username": username,
                "is_active": is_active,
                "user": user,
                "user_uuid": user_uuid,
                "user_username": user_username,
                "user_full_name": user_full_name,
            }
        )
        if agreement_date is not UNSET:
            field_dict["agreement_date"] = agreement_date

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        uuid = UUID(d.pop("uuid"))

        username = d.pop("username")

        is_active = d.pop("is_active")

        user = d.pop("user")

        user_uuid = UUID(d.pop("user_uuid"))

        user_username = d.pop("user_username")

        user_full_name = d.pop("user_full_name")

        _agreement_date = d.pop("agreement_date", UNSET)
        agreement_date: Union[Unset, datetime.datetime]
        if isinstance(_agreement_date, Unset):
            agreement_date = UNSET
        else:
            agreement_date = isoparse(_agreement_date)

        freeipa_profile = cls(
            uuid=uuid,
            username=username,
            is_active=is_active,
            user=user,
            user_uuid=user_uuid,
            user_username=user_username,
            user_full_name=user_full_name,
            agreement_date=agreement_date,
        )

        freeipa_profile.additional_properties = d
        return freeipa_profile

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
