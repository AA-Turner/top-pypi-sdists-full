from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.branch_deletion_outcome import BranchDeletionOutcome
from ..models.branch_deletion_reason import BranchDeletionReason
from ..types import UNSET, Unset






T = TypeVar("T", bound="BranchDeletion")



@_attrs_define
class BranchDeletion:
    """ What happened to the source branch. A fact for the client to word,
    never a reason to treat the merge as failed.

        Attributes:
            outcome (BranchDeletionOutcome): `deleted`: the branch is gone, including when the forge had
                already removed it. `skipped`: it was left alone on purpose,
                see `reason`. `failed`: the forge refused or couldn't be
                reached, and the branch may still exist.
            reason (BranchDeletionReason | Unset): Why a `skipped` branch was left. `fork`: the branch lives in
                another repo. `default_branch`: it is the repo's default
                branch. `protected`: the forge protects it. `in_use`: another
                open pull request in the repo has it as its head or base, so
                deleting it would strand that pull request. `unsupported`: the
                forge's client can't delete branches. Absent unless `outcome`
                is `skipped`.
     """

    outcome: BranchDeletionOutcome
    reason: BranchDeletionReason | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        outcome = self.outcome.value

        reason: str | Unset = UNSET
        if not isinstance(self.reason, Unset):
            reason = self.reason.value



        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "outcome": outcome,
        })
        if reason is not UNSET:
            field_dict["reason"] = reason

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        outcome = BranchDeletionOutcome(d.pop("outcome"))




        _reason = d.pop("reason", UNSET)
        reason: BranchDeletionReason | Unset
        if isinstance(_reason,  Unset):
            reason = UNSET
        else:
            reason = BranchDeletionReason(_reason)




        branch_deletion = cls(
            outcome=outcome,
            reason=reason,
        )


        branch_deletion.additional_properties = d
        return branch_deletion

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
