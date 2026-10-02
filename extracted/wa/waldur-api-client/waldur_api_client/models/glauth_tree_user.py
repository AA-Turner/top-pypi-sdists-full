from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.glauth_tree_membership import GlauthTreeMembership


T = TypeVar("T", bound="GlauthTreeUser")


@_attrs_define
class GlauthTreeUser:
    """
    Attributes:
        username (str):
        uidnumber (Union[None, int]):
        disabled (bool):
        personal_group (Union[None, int]):
        mail (Union[None, str]):
        givenname (Union[None, str]):
        sn (Union[None, str]):
        login_shell (Union[None, str]):
        home_dir (Union[None, str]):
        ssh_keys (list[str]):
        memberships (list['GlauthTreeMembership']):
    """

    username: str
    uidnumber: Union[None, int]
    disabled: bool
    personal_group: Union[None, int]
    mail: Union[None, str]
    givenname: Union[None, str]
    sn: Union[None, str]
    login_shell: Union[None, str]
    home_dir: Union[None, str]
    ssh_keys: list[str]
    memberships: list["GlauthTreeMembership"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        username = self.username

        uidnumber: Union[None, int]
        uidnumber = self.uidnumber

        disabled = self.disabled

        personal_group: Union[None, int]
        personal_group = self.personal_group

        mail: Union[None, str]
        mail = self.mail

        givenname: Union[None, str]
        givenname = self.givenname

        sn: Union[None, str]
        sn = self.sn

        login_shell: Union[None, str]
        login_shell = self.login_shell

        home_dir: Union[None, str]
        home_dir = self.home_dir

        ssh_keys = self.ssh_keys

        memberships = []
        for memberships_item_data in self.memberships:
            memberships_item = memberships_item_data.to_dict()
            memberships.append(memberships_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "username": username,
                "uidnumber": uidnumber,
                "disabled": disabled,
                "personal_group": personal_group,
                "mail": mail,
                "givenname": givenname,
                "sn": sn,
                "login_shell": login_shell,
                "home_dir": home_dir,
                "ssh_keys": ssh_keys,
                "memberships": memberships,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.glauth_tree_membership import GlauthTreeMembership

        d = dict(src_dict)
        username = d.pop("username")

        def _parse_uidnumber(data: object) -> Union[None, int]:
            if data is None:
                return data
            return cast(Union[None, int], data)

        uidnumber = _parse_uidnumber(d.pop("uidnumber"))

        disabled = d.pop("disabled")

        def _parse_personal_group(data: object) -> Union[None, int]:
            if data is None:
                return data
            return cast(Union[None, int], data)

        personal_group = _parse_personal_group(d.pop("personal_group"))

        def _parse_mail(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        mail = _parse_mail(d.pop("mail"))

        def _parse_givenname(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        givenname = _parse_givenname(d.pop("givenname"))

        def _parse_sn(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        sn = _parse_sn(d.pop("sn"))

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

        memberships = []
        _memberships = d.pop("memberships")
        for memberships_item_data in _memberships:
            memberships_item = GlauthTreeMembership.from_dict(memberships_item_data)

            memberships.append(memberships_item)

        glauth_tree_user = cls(
            username=username,
            uidnumber=uidnumber,
            disabled=disabled,
            personal_group=personal_group,
            mail=mail,
            givenname=givenname,
            sn=sn,
            login_shell=login_shell,
            home_dir=home_dir,
            ssh_keys=ssh_keys,
            memberships=memberships,
        )

        glauth_tree_user.additional_properties = d
        return glauth_tree_user

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
