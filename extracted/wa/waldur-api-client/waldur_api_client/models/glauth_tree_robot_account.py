from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="GlauthTreeRobotAccount")


@_attrs_define
class GlauthTreeRobotAccount:
    """
    Attributes:
        username (str):
        uidnumber (Union[None, int]):
        personal_group (Union[None, int]):
        login_shell (Union[None, str]):
        home_dir (Union[None, str]):
        ssh_keys (list[str]):
    """

    username: str
    uidnumber: Union[None, int]
    personal_group: Union[None, int]
    login_shell: Union[None, str]
    home_dir: Union[None, str]
    ssh_keys: list[str]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        username = self.username

        uidnumber: Union[None, int]
        uidnumber = self.uidnumber

        personal_group: Union[None, int]
        personal_group = self.personal_group

        login_shell: Union[None, str]
        login_shell = self.login_shell

        home_dir: Union[None, str]
        home_dir = self.home_dir

        ssh_keys = self.ssh_keys

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "username": username,
                "uidnumber": uidnumber,
                "personal_group": personal_group,
                "login_shell": login_shell,
                "home_dir": home_dir,
                "ssh_keys": ssh_keys,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        username = d.pop("username")

        def _parse_uidnumber(data: object) -> Union[None, int]:
            if data is None:
                return data
            return cast(Union[None, int], data)

        uidnumber = _parse_uidnumber(d.pop("uidnumber"))

        def _parse_personal_group(data: object) -> Union[None, int]:
            if data is None:
                return data
            return cast(Union[None, int], data)

        personal_group = _parse_personal_group(d.pop("personal_group"))

        def _parse_login_shell(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        login_shell = _parse_login_shell(d.pop("login_shell"))

        def _parse_home_dir(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        home_dir = _parse_home_dir(d.pop("home_dir"))

        ssh_keys = cast(list[str], d.pop("ssh_keys"))

        glauth_tree_robot_account = cls(
            username=username,
            uidnumber=uidnumber,
            personal_group=personal_group,
            login_shell=login_shell,
            home_dir=home_dir,
            ssh_keys=ssh_keys,
        )

        glauth_tree_robot_account.additional_properties = d
        return glauth_tree_robot_account

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
