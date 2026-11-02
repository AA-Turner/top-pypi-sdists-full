from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.replace_git_hub_runtime_bindings_request_repositories_item import (
        ReplaceGitHubRuntimeBindingsRequestRepositoriesItem,
    )


T = TypeVar("T", bound="ReplaceGitHubRuntimeBindingsRequest")


@_attrs_define
class ReplaceGitHubRuntimeBindingsRequest:
    """
    Attributes:
        repositories (list[ReplaceGitHubRuntimeBindingsRequestRepositoriesItem]):
    """

    repositories: list[ReplaceGitHubRuntimeBindingsRequestRepositoriesItem]

    def to_dict(self) -> dict[str, Any]:
        repositories = []
        for repositories_item_data in self.repositories:
            repositories_item = repositories_item_data.to_dict()
            repositories.append(repositories_item)

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "repositories": repositories,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.replace_git_hub_runtime_bindings_request_repositories_item import (
            ReplaceGitHubRuntimeBindingsRequestRepositoriesItem,
        )

        d = dict(src_dict)
        repositories = []
        _repositories = d.pop("repositories")
        for repositories_item_data in _repositories:
            repositories_item = (
                ReplaceGitHubRuntimeBindingsRequestRepositoriesItem.from_dict(
                    repositories_item_data
                )
            )

            repositories.append(repositories_item)

        replace_git_hub_runtime_bindings_request = cls(
            repositories=repositories,
        )

        return replace_git_hub_runtime_bindings_request
