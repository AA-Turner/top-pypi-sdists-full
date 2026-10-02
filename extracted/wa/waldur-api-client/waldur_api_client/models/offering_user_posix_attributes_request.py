from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="OfferingUserPosixAttributesRequest")


@_attrs_define
class OfferingUserPosixAttributesRequest:
    """
    Attributes:
        login_shell (Union[Unset, str]): Login shell for this account (LDAP loginShell).
        home_directory (Union[Unset, str]): Home directory for this account (LDAP homeDirectory).
        uidnumber (Union[None, Unset, int]): Override the account's UID. The value must fall within the offering's
            resolved POSIX ID pool and is rejected with 400 if it is out of range or already held by another active
            identity.
        primarygroup (Union[None, Unset, int]): Override the account's primary GID, under the same pool-range and
            uniqueness rules as uidnumber.
    """

    login_shell: Union[Unset, str] = UNSET
    home_directory: Union[Unset, str] = UNSET
    uidnumber: Union[None, Unset, int] = UNSET
    primarygroup: Union[None, Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        login_shell = self.login_shell

        home_directory = self.home_directory

        uidnumber: Union[None, Unset, int]
        if isinstance(self.uidnumber, Unset):
            uidnumber = UNSET
        else:
            uidnumber = self.uidnumber

        primarygroup: Union[None, Unset, int]
        if isinstance(self.primarygroup, Unset):
            primarygroup = UNSET
        else:
            primarygroup = self.primarygroup

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if login_shell is not UNSET:
            field_dict["login_shell"] = login_shell
        if home_directory is not UNSET:
            field_dict["home_directory"] = home_directory
        if uidnumber is not UNSET:
            field_dict["uidnumber"] = uidnumber
        if primarygroup is not UNSET:
            field_dict["primarygroup"] = primarygroup

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        login_shell = d.pop("login_shell", UNSET)

        home_directory = d.pop("home_directory", UNSET)

        def _parse_uidnumber(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        uidnumber = _parse_uidnumber(d.pop("uidnumber", UNSET))

        def _parse_primarygroup(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        primarygroup = _parse_primarygroup(d.pop("primarygroup", UNSET))

        offering_user_posix_attributes_request = cls(
            login_shell=login_shell,
            home_directory=home_directory,
            uidnumber=uidnumber,
            primarygroup=primarygroup,
        )

        offering_user_posix_attributes_request.additional_properties = d
        return offering_user_posix_attributes_request

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
