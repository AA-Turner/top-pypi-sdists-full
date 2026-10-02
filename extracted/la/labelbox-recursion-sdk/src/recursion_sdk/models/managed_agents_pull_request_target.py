from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="ManagedAgentsPullRequestTarget")



@_attrs_define
class ManagedAgentsPullRequestTarget:
    """ The exact, immutable identity of one GitHub pull request under automation: the repository, the number, and the two
    commits that bound the reviewed diff.

        Example:
            {'base_sha': 'example', 'head_sha': 'example', 'number': 1, 'owner': 'example', 'repository': 'example',
                'repository_id': 1}

        Attributes:
            base_sha (str): Base commit the pull request targets, as a lowercase 40-character hex SHA. Always differs from
                head_sha.
            head_sha (str): Head commit under review, as a lowercase 40-character hex SHA. The sandbox stages exactly this
                tree, so the review cannot drift onto a later push.
            number (int): Pull request number within the repository.
            owner (str): GitHub account or organization that owns the repository. Must match the connected App installation
                account.
            repository (str): GitHub repository name, without the owner prefix.
            repository_id (int): Immutable GitHub repository id, read from GitHub rather than from the request path so a
                later rename or transfer cannot make the stored owner and name identify a different repository.
     """

    base_sha: str
    head_sha: str
    number: int
    owner: str
    repository: str
    repository_id: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        base_sha = self.base_sha

        head_sha = self.head_sha

        number = self.number

        owner = self.owner

        repository = self.repository

        repository_id = self.repository_id


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "base_sha": base_sha,
            "head_sha": head_sha,
            "number": number,
            "owner": owner,
            "repository": repository,
            "repository_id": repository_id,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        base_sha = d.pop("base_sha")

        head_sha = d.pop("head_sha")

        number = d.pop("number")

        owner = d.pop("owner")

        repository = d.pop("repository")

        repository_id = d.pop("repository_id")

        managed_agents_pull_request_target = cls(
            base_sha=base_sha,
            head_sha=head_sha,
            number=number,
            owner=owner,
            repository=repository,
            repository_id=repository_id,
        )


        managed_agents_pull_request_target.additional_properties = d
        return managed_agents_pull_request_target

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
