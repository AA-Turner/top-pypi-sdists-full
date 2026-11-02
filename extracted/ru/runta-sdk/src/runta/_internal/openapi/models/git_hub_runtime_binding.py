from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="GitHubRuntimeBinding")


@_attrs_define
class GitHubRuntimeBinding:
    """
    Attributes:
        id (str):
        tenant_id (str):
        runtime_id (str):
        repository_id (int):
        branch (str):
        sort_order (int):
    """

    id: str
    tenant_id: str
    runtime_id: str
    repository_id: int
    branch: str
    sort_order: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        tenant_id = self.tenant_id

        runtime_id = self.runtime_id

        repository_id = self.repository_id

        branch = self.branch

        sort_order = self.sort_order

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "tenant_id": tenant_id,
                "runtime_id": runtime_id,
                "repository_id": repository_id,
                "branch": branch,
                "sort_order": sort_order,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        tenant_id = d.pop("tenant_id")

        runtime_id = d.pop("runtime_id")

        repository_id = d.pop("repository_id")

        branch = d.pop("branch")

        sort_order = d.pop("sort_order")

        git_hub_runtime_binding = cls(
            id=id,
            tenant_id=tenant_id,
            runtime_id=runtime_id,
            repository_id=repository_id,
            branch=branch,
            sort_order=sort_order,
        )

        git_hub_runtime_binding.additional_properties = d
        return git_hub_runtime_binding

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
