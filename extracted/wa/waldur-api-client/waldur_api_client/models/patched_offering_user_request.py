from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="PatchedOfferingUserRequest")


@_attrs_define
class PatchedOfferingUserRequest:
    """
    Attributes:
        user (Union[Unset, str]):
        offering (Union[Unset, str]):
        username (Union[None, Unset, str]):
        offering_uuid (Union[Unset, UUID]):
        user_uuid (Union[Unset, UUID]):
    """

    user: Union[Unset, str] = UNSET
    offering: Union[Unset, str] = UNSET
    username: Union[None, Unset, str] = UNSET
    offering_uuid: Union[Unset, UUID] = UNSET
    user_uuid: Union[Unset, UUID] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        user = self.user

        offering = self.offering

        username: Union[None, Unset, str]
        if isinstance(self.username, Unset):
            username = UNSET
        else:
            username = self.username

        offering_uuid: Union[Unset, str] = UNSET
        if not isinstance(self.offering_uuid, Unset):
            offering_uuid = str(self.offering_uuid)

        user_uuid: Union[Unset, str] = UNSET
        if not isinstance(self.user_uuid, Unset):
            user_uuid = str(self.user_uuid)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if user is not UNSET:
            field_dict["user"] = user
        if offering is not UNSET:
            field_dict["offering"] = offering
        if username is not UNSET:
            field_dict["username"] = username
        if offering_uuid is not UNSET:
            field_dict["offering_uuid"] = offering_uuid
        if user_uuid is not UNSET:
            field_dict["user_uuid"] = user_uuid

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        user = d.pop("user", UNSET)

        offering = d.pop("offering", UNSET)

        def _parse_username(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        username = _parse_username(d.pop("username", UNSET))

        _offering_uuid = d.pop("offering_uuid", UNSET)
        offering_uuid: Union[Unset, UUID]
        if isinstance(_offering_uuid, Unset):
            offering_uuid = UNSET
        else:
            offering_uuid = UUID(_offering_uuid)

        _user_uuid = d.pop("user_uuid", UNSET)
        user_uuid: Union[Unset, UUID]
        if isinstance(_user_uuid, Unset):
            user_uuid = UNSET
        else:
            user_uuid = UUID(_user_uuid)

        patched_offering_user_request = cls(
            user=user,
            offering=offering,
            username=username,
            offering_uuid=offering_uuid,
            user_uuid=user_uuid,
        )

        patched_offering_user_request.additional_properties = d
        return patched_offering_user_request

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
