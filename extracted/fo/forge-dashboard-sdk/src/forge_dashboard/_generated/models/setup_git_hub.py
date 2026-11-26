from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.setup_installation import SetupInstallation





T = TypeVar("T", bound="SetupGitHub")



@_attrs_define
class SetupGitHub:
    """ 
        Attributes:
            configured (bool): Whether this server has the GitHub App's OAuth client. Without it nothing here can start.
            install_url (str): Where the App is installed (`github.com/apps/<slug>/installations/new`). Empty when the
                server doesn't know the App's slug (`GITHUB_APP_SLUG`).
            authorized (bool):
            account (str): The authorized account's login, or empty.
            installations (list[SetupInstallation]):
            installations_unavailable (bool):
            repository_count (int): Repositories the board sees on GitHub as of its last refresh.
     """

    configured: bool
    install_url: str
    authorized: bool
    account: str
    installations: list[SetupInstallation]
    installations_unavailable: bool
    repository_count: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.setup_installation import SetupInstallation # noqa: PLC0415
        configured = self.configured

        install_url = self.install_url

        authorized = self.authorized

        account = self.account

        installations = []
        for installations_item_data in self.installations:
            installations_item = installations_item_data.to_dict()
            installations.append(installations_item)



        installations_unavailable = self.installations_unavailable

        repository_count = self.repository_count


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "configured": configured,
            "installUrl": install_url,
            "authorized": authorized,
            "account": account,
            "installations": installations,
            "installationsUnavailable": installations_unavailable,
            "repositoryCount": repository_count,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.setup_installation import SetupInstallation # noqa: PLC0415
        d = dict(src_dict)
        configured = d.pop("configured")

        install_url = d.pop("installUrl")

        authorized = d.pop("authorized")

        account = d.pop("account")

        installations = []
        _installations = d.pop("installations")
        for installations_item_data in (_installations):
            installations_item = SetupInstallation.from_dict(installations_item_data)



            installations.append(installations_item)


        installations_unavailable = d.pop("installationsUnavailable")

        repository_count = d.pop("repositoryCount")

        setup_git_hub = cls(
            configured=configured,
            install_url=install_url,
            authorized=authorized,
            account=account,
            installations=installations,
            installations_unavailable=installations_unavailable,
            repository_count=repository_count,
        )


        setup_git_hub.additional_properties = d
        return setup_git_hub

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
