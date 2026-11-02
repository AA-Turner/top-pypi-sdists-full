from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="GitHubInstallation")


@_attrs_define
class GitHubInstallation:
    """
    Attributes:
        installation_id (int):
        account_login (str):
        account_type (str):
        account_avatar_url (str):
        repository_selection (str):
    """

    installation_id: int
    account_login: str
    account_type: str
    account_avatar_url: str
    repository_selection: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        installation_id = self.installation_id

        account_login = self.account_login

        account_type = self.account_type

        account_avatar_url = self.account_avatar_url

        repository_selection = self.repository_selection

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "installation_id": installation_id,
                "account_login": account_login,
                "account_type": account_type,
                "account_avatar_url": account_avatar_url,
                "repository_selection": repository_selection,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        installation_id = d.pop("installation_id")

        account_login = d.pop("account_login")

        account_type = d.pop("account_type")

        account_avatar_url = d.pop("account_avatar_url")

        repository_selection = d.pop("repository_selection")

        git_hub_installation = cls(
            installation_id=installation_id,
            account_login=account_login,
            account_type=account_type,
            account_avatar_url=account_avatar_url,
            repository_selection=repository_selection,
        )

        git_hub_installation.additional_properties = d
        return git_hub_installation

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
