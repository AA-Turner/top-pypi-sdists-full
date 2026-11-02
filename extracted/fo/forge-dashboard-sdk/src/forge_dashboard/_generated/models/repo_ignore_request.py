from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.forge import Forge






T = TypeVar("T", bound="RepoIgnoreRequest")



@_attrs_define
class RepoIgnoreRequest:
    """ Which repo to ignore, and in which scope(s). At least one
    of prs/issues must be true — a request with both false is
    rejected with 400 rather than silently doing nothing; use POST
    /api/v1/repos/unignore to clear both at once instead.

        Attributes:
            forge (Forge):
            full_name (str): "owner/repo", matching a Repo.fullName from GET /api/v1/dashboard.
            prs (bool): Whether to ignore this repo's pull requests.
            issues (bool): Whether to ignore this repo's issues.
     """

    forge: Forge
    full_name: str
    prs: bool
    issues: bool
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        forge = self.forge.value

        full_name = self.full_name

        prs = self.prs

        issues = self.issues


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "forge": forge,
            "fullName": full_name,
            "prs": prs,
            "issues": issues,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        forge = Forge(d.pop("forge"))




        full_name = d.pop("fullName")

        prs = d.pop("prs")

        issues = d.pop("issues")

        repo_ignore_request = cls(
            forge=forge,
            full_name=full_name,
            prs=prs,
            issues=issues,
        )


        repo_ignore_request.additional_properties = d
        return repo_ignore_request

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
