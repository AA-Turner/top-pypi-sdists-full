from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="ManagedAgentsRepository")



@_attrs_define
class ManagedAgentsRepository:
    """ One GitHub repository an integration connection's install can reach, as reported by GitHub. Returned when listing a
    connection's repositories to scope a grant.

        Example:
            {'archived': True, 'default_branch': 'example', 'full_name': 'example', 'id': 1, 'name': 'example-name',
                'private': True}

        Attributes:
            full_name (str): Owner-qualified repository name, for example "acme/platform". This is the form a vault grant's
                repository selection uses.
            id (int): Stable numeric GitHub repository id used to bind automation to an immutable repository identity.
            name (str): Repository name without its owner, for example "platform".
            private (bool): Whether the repository is private on GitHub.
            archived (bool | Unset): Whether the repository is archived on GitHub and therefore read-only there.
            default_branch (str | Unset): Branch GitHub reports as the repository default, for example "main". Absent when
                GitHub reports none, as for an empty repository.
     """

    full_name: str
    id: int
    name: str
    private: bool
    archived: bool | Unset = UNSET
    default_branch: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        full_name = self.full_name

        id = self.id

        name = self.name

        private = self.private

        archived = self.archived

        default_branch = self.default_branch


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "full_name": full_name,
            "id": id,
            "name": name,
            "private": private,
        })
        if archived is not UNSET:
            field_dict["archived"] = archived
        if default_branch is not UNSET:
            field_dict["default_branch"] = default_branch

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        full_name = d.pop("full_name")

        id = d.pop("id")

        name = d.pop("name")

        private = d.pop("private")

        archived = d.pop("archived", UNSET)

        default_branch = d.pop("default_branch", UNSET)

        managed_agents_repository = cls(
            full_name=full_name,
            id=id,
            name=name,
            private=private,
            archived=archived,
            default_branch=default_branch,
        )


        managed_agents_repository.additional_properties = d
        return managed_agents_repository

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
