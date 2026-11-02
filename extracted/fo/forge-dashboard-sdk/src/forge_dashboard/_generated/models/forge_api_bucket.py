from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.forge import Forge






T = TypeVar("T", bound="ForgeApiBucket")



@_attrs_define
class ForgeApiBucket:
    """ 
        Attributes:
            forge (Forge):
            credential (str): The credential the requests were made with, as a label with no secret and no user id.
            kind (str): Why the requests were made. Open-ended, so a new kind is not a breaking change; today `full`,
                `scoped_webhook`, `ci_poll`, `auto_merge_poll`, `details`, `hook_maintenance`, `advisories`, `user_action` and
                `unknown`.
            repo (str): The repository as `owner/name`, or empty when the request touched no single repository. `other`
                collects the repositories past the cap on how many are counted separately.
            rest (int): REST requests that were charged against the REST budget.
            graphql (int): GraphQL requests made.
            graphql_cost (int): The `rateLimit.cost` points the GraphQL requests were charged.
            not_modified (int): Requests answered `304 Not Modified`, which cost nothing.
     """

    forge: Forge
    credential: str
    kind: str
    repo: str
    rest: int
    graphql: int
    graphql_cost: int
    not_modified: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        forge = self.forge.value

        credential = self.credential

        kind = self.kind

        repo = self.repo

        rest = self.rest

        graphql = self.graphql

        graphql_cost = self.graphql_cost

        not_modified = self.not_modified


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "forge": forge,
            "credential": credential,
            "kind": kind,
            "repo": repo,
            "rest": rest,
            "graphql": graphql,
            "graphqlCost": graphql_cost,
            "notModified": not_modified,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        forge = Forge(d.pop("forge"))




        credential = d.pop("credential")

        kind = d.pop("kind")

        repo = d.pop("repo")

        rest = d.pop("rest")

        graphql = d.pop("graphql")

        graphql_cost = d.pop("graphqlCost")

        not_modified = d.pop("notModified")

        forge_api_bucket = cls(
            forge=forge,
            credential=credential,
            kind=kind,
            repo=repo,
            rest=rest,
            graphql=graphql,
            graphql_cost=graphql_cost,
            not_modified=not_modified,
        )


        forge_api_bucket.additional_properties = d
        return forge_api_bucket

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
