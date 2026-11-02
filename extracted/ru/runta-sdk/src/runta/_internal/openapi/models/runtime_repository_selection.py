from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

from ..types import UNSET, Unset

T = TypeVar("T", bound="RuntimeRepositorySelection")


@_attrs_define
class RuntimeRepositorySelection:
    """
    Attributes:
        repository_id (int):
        branch (None | str | Unset):
    """

    repository_id: int
    branch: None | str | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        repository_id = self.repository_id

        branch: None | str | Unset
        if isinstance(self.branch, Unset):
            branch = UNSET
        else:
            branch = self.branch

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "repository_id": repository_id,
            }
        )
        if branch is not UNSET:
            field_dict["branch"] = branch

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        repository_id = d.pop("repository_id")

        def _parse_branch(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        branch = _parse_branch(d.pop("branch", UNSET))

        runtime_repository_selection = cls(
            repository_id=repository_id,
            branch=branch,
        )

        return runtime_repository_selection
