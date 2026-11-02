from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.git_hub_installation import GitHubInstallation
    from ..models.git_hub_repository import GitHubRepository


T = TypeVar("T", bound="GitHubRepositoryList")


@_attrs_define
class GitHubRepositoryList:
    """
    Attributes:
        repositories (list[GitHubRepository]):
        next_page_token (None | str):
        installations (list[GitHubInstallation]):
    """

    repositories: list[GitHubRepository]
    next_page_token: None | str
    installations: list[GitHubInstallation]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        repositories = []
        for repositories_item_data in self.repositories:
            repositories_item = repositories_item_data.to_dict()
            repositories.append(repositories_item)

        next_page_token: None | str
        next_page_token = self.next_page_token

        installations = []
        for installations_item_data in self.installations:
            installations_item = installations_item_data.to_dict()
            installations.append(installations_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "repositories": repositories,
                "next_page_token": next_page_token,
                "installations": installations,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.git_hub_installation import GitHubInstallation
        from ..models.git_hub_repository import GitHubRepository

        d = dict(src_dict)
        repositories = []
        _repositories = d.pop("repositories")
        for repositories_item_data in _repositories:
            repositories_item = GitHubRepository.from_dict(repositories_item_data)

            repositories.append(repositories_item)

        def _parse_next_page_token(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        next_page_token = _parse_next_page_token(d.pop("next_page_token"))

        installations = []
        _installations = d.pop("installations")
        for installations_item_data in _installations:
            installations_item = GitHubInstallation.from_dict(installations_item_data)

            installations.append(installations_item)

        git_hub_repository_list = cls(
            repositories=repositories,
            next_page_token=next_page_token,
            installations=installations,
        )

        git_hub_repository_list.additional_properties = d
        return git_hub_repository_list

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
