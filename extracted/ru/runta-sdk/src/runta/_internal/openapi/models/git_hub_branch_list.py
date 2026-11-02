from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.git_hub_branch import GitHubBranch


T = TypeVar("T", bound="GitHubBranchList")


@_attrs_define
class GitHubBranchList:
    """
    Attributes:
        branches (list[GitHubBranch]):
    """

    branches: list[GitHubBranch]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        branches = []
        for branches_item_data in self.branches:
            branches_item = branches_item_data.to_dict()
            branches.append(branches_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "branches": branches,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.git_hub_branch import GitHubBranch

        d = dict(src_dict)
        branches = []
        _branches = d.pop("branches")
        for branches_item_data in _branches:
            branches_item = GitHubBranch.from_dict(branches_item_data)

            branches.append(branches_item)

        git_hub_branch_list = cls(
            branches=branches,
        )

        git_hub_branch_list.additional_properties = d
        return git_hub_branch_list

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
