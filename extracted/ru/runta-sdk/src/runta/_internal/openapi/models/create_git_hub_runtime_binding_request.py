from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="CreateGitHubRuntimeBindingRequest")


@_attrs_define
class CreateGitHubRuntimeBindingRequest:
    """
    Attributes:
        runtime_id (str):
        repository_id (int):
        branch (str):
    """

    runtime_id: str
    repository_id: int
    branch: str

    def to_dict(self) -> dict[str, Any]:
        runtime_id = self.runtime_id

        repository_id = self.repository_id

        branch = self.branch

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "runtime_id": runtime_id,
                "repository_id": repository_id,
                "branch": branch,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        runtime_id = d.pop("runtime_id")

        repository_id = d.pop("repository_id")

        branch = d.pop("branch")

        create_git_hub_runtime_binding_request = cls(
            runtime_id=runtime_id,
            repository_id=repository_id,
            branch=branch,
        )

        return create_git_hub_runtime_binding_request
