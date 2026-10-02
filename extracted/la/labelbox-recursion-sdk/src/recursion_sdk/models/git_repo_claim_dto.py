from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="GitRepoClaimDto")



@_attrs_define
class GitRepoClaimDto:
    """ A provisioned per-Aligner Forgejo repo claim: clone URL, default branch, and a push token.

        Example:
            {'cloneUrl': 'http://localhost:3050/aligner-a1b2c3d4e5f6/problem-784e2386.git', 'defaultBranch': 'main',
                'pushToken': '<example-push-token-not-a-real-value>'}

        Attributes:
            clone_url (str): HTTP(S) clone URL for the claimed repo.
            default_branch (str): The repo's default branch name.
            push_token (str): Forgejo access token for this claim's Aligner user, granting write access to every repo that
                user owns. Does not expire by default; a later claim by the same Aligner rotates it, invalidating this value.
                Returned once; not stored.
     """

    clone_url: str
    default_branch: str
    push_token: str





    def to_dict(self) -> dict[str, Any]:
        clone_url = self.clone_url

        default_branch = self.default_branch

        push_token = self.push_token


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "cloneUrl": clone_url,
            "defaultBranch": default_branch,
            "pushToken": push_token,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        clone_url = d.pop("cloneUrl")

        default_branch = d.pop("defaultBranch")

        push_token = d.pop("pushToken")

        git_repo_claim_dto = cls(
            clone_url=clone_url,
            default_branch=default_branch,
            push_token=push_token,
        )

        return git_repo_claim_dto

