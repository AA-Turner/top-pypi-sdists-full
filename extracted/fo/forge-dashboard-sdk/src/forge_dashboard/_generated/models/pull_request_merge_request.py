from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.forge import Forge
from ..types import UNSET, Unset






T = TypeVar("T", bound="PullRequestMergeRequest")



@_attrs_define
class PullRequestMergeRequest:
    """ Which pull request to merge, and whether to delete its source branch afterwards.

        Attributes:
            forge (Forge):
            full_name (str): "owner/repo", matching a Repo.fullName from GET /api/v1/dashboard.
            number (int): Matching a PullRequest.number from GET /api/v1/dashboard.
            delete_branch (bool | Unset): Delete the source branch once the merge has landed. Default: False.
     """

    forge: Forge
    full_name: str
    number: int
    delete_branch: bool | Unset = False
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        forge = self.forge.value

        full_name = self.full_name

        number = self.number

        delete_branch = self.delete_branch


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "forge": forge,
            "fullName": full_name,
            "number": number,
        })
        if delete_branch is not UNSET:
            field_dict["deleteBranch"] = delete_branch

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        forge = Forge(d.pop("forge"))




        full_name = d.pop("fullName")

        number = d.pop("number")

        delete_branch = d.pop("deleteBranch", UNSET)

        pull_request_merge_request = cls(
            forge=forge,
            full_name=full_name,
            number=number,
            delete_branch=delete_branch,
        )


        pull_request_merge_request.additional_properties = d
        return pull_request_merge_request

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
