from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="AccountRename")


@_attrs_define
class AccountRename:
    """
    Attributes:
        username (str):
        new_username (Union[None, str]): Null when the rename would first allocate a POSIX UID.
        home_directory (str):
        new_home_directory (str):
    """

    username: str
    new_username: Union[None, str]
    home_directory: str
    new_home_directory: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        username = self.username

        new_username: Union[None, str]
        new_username = self.new_username

        home_directory = self.home_directory

        new_home_directory = self.new_home_directory

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "username": username,
                "new_username": new_username,
                "home_directory": home_directory,
                "new_home_directory": new_home_directory,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        username = d.pop("username")

        def _parse_new_username(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        new_username = _parse_new_username(d.pop("new_username"))

        home_directory = d.pop("home_directory")

        new_home_directory = d.pop("new_home_directory")

        account_rename = cls(
            username=username,
            new_username=new_username,
            home_directory=home_directory,
            new_home_directory=new_home_directory,
        )

        account_rename.additional_properties = d
        return account_rename

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
