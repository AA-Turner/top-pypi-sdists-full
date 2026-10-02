from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from uuid import UUID






T = TypeVar("T", bound="CreateGitRepoClaimDto")



@_attrs_define
class CreateGitRepoClaimDto:
    """ Request body for claiming a per-Aligner Forgejo repo for a coding task. The claiming Aligner is the authenticated
    caller — never a client-supplied identity — so one caller can never claim a repo under another Aligner’s identity.

        Example:
            {'problemId': '784e2386-e297-4f9d-a886-838422383b65'}

        Attributes:
            problem_id (UUID): The problem this claim is for.
     """

    problem_id: UUID
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        problem_id = str(self.problem_id)


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "problemId": problem_id,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        problem_id = UUID(d.pop("problemId"))




        create_git_repo_claim_dto = cls(
            problem_id=problem_id,
        )


        create_git_repo_claim_dto.additional_properties = d
        return create_git_repo_claim_dto

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
