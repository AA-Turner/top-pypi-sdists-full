from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="UserChecklistCompletionOfferingUser")


@_attrs_define
class UserChecklistCompletionOfferingUser:
    """
    Attributes:
        uuid (UUID):
        user_full_name (str):
        user_email (str):
        state (str):
        username (Union[None, Unset, str]):
        is_restricted (Union[Unset, bool]): Signal to service if the user account is restricted or not
    """

    uuid: UUID
    user_full_name: str
    user_email: str
    state: str
    username: Union[None, Unset, str] = UNSET
    is_restricted: Union[Unset, bool] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid = str(self.uuid)

        user_full_name = self.user_full_name

        user_email = self.user_email

        state = self.state

        username: Union[None, Unset, str]
        if isinstance(self.username, Unset):
            username = UNSET
        else:
            username = self.username

        is_restricted = self.is_restricted

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uuid": uuid,
                "user_full_name": user_full_name,
                "user_email": user_email,
                "state": state,
            }
        )
        if username is not UNSET:
            field_dict["username"] = username
        if is_restricted is not UNSET:
            field_dict["is_restricted"] = is_restricted

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        uuid = UUID(d.pop("uuid"))

        user_full_name = d.pop("user_full_name")

        user_email = d.pop("user_email")

        state = d.pop("state")

        def _parse_username(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        username = _parse_username(d.pop("username", UNSET))

        is_restricted = d.pop("is_restricted", UNSET)

        user_checklist_completion_offering_user = cls(
            uuid=uuid,
            user_full_name=user_full_name,
            user_email=user_email,
            state=state,
            username=username,
            is_restricted=is_restricted,
        )

        user_checklist_completion_offering_user.additional_properties = d
        return user_checklist_completion_offering_user

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
