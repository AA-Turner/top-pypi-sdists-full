from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.create_check_fix_cycle_dto_target_type_0_kind import CreateCheckFixCycleDtoTargetType0Kind






T = TypeVar("T", bound="CreateCheckFixCycleDtoTargetType0")



@_attrs_define
class CreateCheckFixCycleDtoTargetType0:
    """ 
        Attributes:
            kind (CreateCheckFixCycleDtoTargetType0Kind): Discriminator for the git_fork target arm.
            fork_repo (str): Fork repository identifier the fix agent pushes to, e.g. "owner/repo".
            base_sha (str): Base commit SHA the fork PR is opened against, pinned for the whole cycle.
            head_sha (str): Head commit SHA of the fork PR at cycle start. Advances only through check consensus, never a
                fix child's own claim.
            head_ref (str): The fork branch name whose current tip a branch-tip-mode check clones, and the same branch a fix
                child pushes fixes onto.
            problem_dir (str): Git-repo-relative directory of the problem under repair, e.g. "problems/channel-diffuser-
                design".
     """

    kind: CreateCheckFixCycleDtoTargetType0Kind
    fork_repo: str
    base_sha: str
    head_sha: str
    head_ref: str
    problem_dir: str





    def to_dict(self) -> dict[str, Any]:
        kind = self.kind.value

        fork_repo = self.fork_repo

        base_sha = self.base_sha

        head_sha = self.head_sha

        head_ref = self.head_ref

        problem_dir = self.problem_dir


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "kind": kind,
            "forkRepo": fork_repo,
            "baseSha": base_sha,
            "headSha": head_sha,
            "headRef": head_ref,
            "problemDir": problem_dir,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        kind = CreateCheckFixCycleDtoTargetType0Kind(d.pop("kind"))




        fork_repo = d.pop("forkRepo")

        base_sha = d.pop("baseSha")

        head_sha = d.pop("headSha")

        head_ref = d.pop("headRef")

        problem_dir = d.pop("problemDir")

        create_check_fix_cycle_dto_target_type_0 = cls(
            kind=kind,
            fork_repo=fork_repo,
            base_sha=base_sha,
            head_sha=head_sha,
            head_ref=head_ref,
            problem_dir=problem_dir,
        )

        return create_check_fix_cycle_dto_target_type_0

