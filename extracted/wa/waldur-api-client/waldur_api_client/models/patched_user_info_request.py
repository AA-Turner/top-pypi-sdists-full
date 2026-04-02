from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="PatchedUserInfoRequest")


@_attrs_define
class PatchedUserInfoRequest:
    """
    Attributes:
        shortname (Union[None, Unset, str]): A short, unique name for you. It will be used to form your local username
            on any systems. Should only contain lower-case letters and digits and must start with a letter.
        user (Union[Unset, str]):
    """

    shortname: Union[None, Unset, str] = UNSET
    user: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        shortname: Union[None, Unset, str]
        if isinstance(self.shortname, Unset):
            shortname = UNSET
        else:
            shortname = self.shortname

        user = self.user

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if shortname is not UNSET:
            field_dict["shortname"] = shortname
        if user is not UNSET:
            field_dict["user"] = user

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_shortname(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        shortname = _parse_shortname(d.pop("shortname", UNSET))

        user = d.pop("user", UNSET)

        patched_user_info_request = cls(
            shortname=shortname,
            user=user,
        )

        patched_user_info_request.additional_properties = d
        return patched_user_info_request

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
