from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="ReplaceGitHubRuntimeBindingsRequestRepositoriesItem")


@_attrs_define
class ReplaceGitHubRuntimeBindingsRequestRepositoriesItem:
    """
    Attributes:
        repository_id (int):
        branch (str):
    """

    repository_id: int
    branch: str

    def to_dict(self) -> dict[str, Any]:
        repository_id = self.repository_id

        branch = self.branch

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "repository_id": repository_id,
                "branch": branch,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        repository_id = d.pop("repository_id")

        branch = d.pop("branch")

        replace_git_hub_runtime_bindings_request_repositories_item = cls(
            repository_id=repository_id,
            branch=branch,
        )

        return replace_git_hub_runtime_bindings_request_repositories_item
