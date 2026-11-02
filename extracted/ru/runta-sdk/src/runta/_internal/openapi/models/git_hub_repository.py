from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="GitHubRepository")


@_attrs_define
class GitHubRepository:
    """
    Attributes:
        id (int):
        installation_id (int):
        owner (str):
        name (str):
        default_branch (str):
        private (bool):
    """

    id: int
    installation_id: int
    owner: str
    name: str
    default_branch: str
    private: bool
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        installation_id = self.installation_id

        owner = self.owner

        name = self.name

        default_branch = self.default_branch

        private = self.private

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "installation_id": installation_id,
                "owner": owner,
                "name": name,
                "default_branch": default_branch,
                "private": private,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        installation_id = d.pop("installation_id")

        owner = d.pop("owner")

        name = d.pop("name")

        default_branch = d.pop("default_branch")

        private = d.pop("private")

        git_hub_repository = cls(
            id=id,
            installation_id=installation_id,
            owner=owner,
            name=name,
            default_branch=default_branch,
            private=private,
        )

        git_hub_repository.additional_properties = d
        return git_hub_repository

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
