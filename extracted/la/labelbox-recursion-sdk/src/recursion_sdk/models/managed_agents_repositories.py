from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.managed_agents_repository import ManagedAgentsRepository





T = TypeVar("T", bound="ManagedAgentsRepositories")



@_attrs_define
class ManagedAgentsRepositories:
    """ One page of the repositories a GitHub integration connection can reach. Returned to populate a repository picker
    when scoping a vault grant.

        Example:
            {'page': 1, 'repositories': [{'archived': True, 'default_branch': 'example', 'full_name': 'example', 'id': 1,
                'name': 'example-name', 'private': True}], 'total_count': 1}

        Attributes:
            page (int): 1-based page this response covers. Defaults to 1 when the request omits or under-specifies it.
            repositories (list[ManagedAgentsRepository] | None): Repositories reachable on this page, up to 100 per page.
            total_count (int): Total repositories the connection can reach across all pages, as reported by GitHub.
     """

    page: int
    repositories: list[ManagedAgentsRepository] | None
    total_count: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.managed_agents_repository import ManagedAgentsRepository # noqa: PLC0415
        page = self.page

        repositories: list[dict[str, Any]] | None
        if isinstance(self.repositories, list):
            repositories = []
            for repositories_type_0_item_data in self.repositories:
                repositories_type_0_item = repositories_type_0_item_data.to_dict()
                repositories.append(repositories_type_0_item)


        else:
            repositories = self.repositories

        total_count = self.total_count


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "page": page,
            "repositories": repositories,
            "total_count": total_count,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.managed_agents_repository import ManagedAgentsRepository # noqa: PLC0415
        d = dict(src_dict)
        page = d.pop("page")

        def _parse_repositories(data: object) -> list[ManagedAgentsRepository] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                repositories_type_0 = []
                _repositories_type_0 = data
                for repositories_type_0_item_data in (_repositories_type_0):
                    repositories_type_0_item = ManagedAgentsRepository.from_dict(repositories_type_0_item_data)



                    repositories_type_0.append(repositories_type_0_item)

                return repositories_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[ManagedAgentsRepository] | None, data)

        repositories = _parse_repositories(d.pop("repositories"))


        total_count = d.pop("total_count")

        managed_agents_repositories = cls(
            page=page,
            repositories=repositories,
            total_count=total_count,
        )


        managed_agents_repositories.additional_properties = d
        return managed_agents_repositories

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
