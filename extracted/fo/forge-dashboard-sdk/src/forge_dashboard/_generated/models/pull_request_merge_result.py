from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.branch_deletion import BranchDeletion





T = TypeVar("T", bound="PullRequestMergeResult")



@_attrs_define
class PullRequestMergeResult:
    """ What a merge that asked for `deleteBranch` did besides merging.

        Attributes:
            branch_deletion (BranchDeletion): What happened to the source branch. A fact for the client to word,
                never a reason to treat the merge as failed.
     """

    branch_deletion: BranchDeletion
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.branch_deletion import BranchDeletion # noqa: PLC0415
        branch_deletion = self.branch_deletion.to_dict()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "branchDeletion": branch_deletion,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.branch_deletion import BranchDeletion # noqa: PLC0415
        d = dict(src_dict)
        branch_deletion = BranchDeletion.from_dict(d.pop("branchDeletion"))




        pull_request_merge_result = cls(
            branch_deletion=branch_deletion,
        )


        pull_request_merge_result.additional_properties = d
        return pull_request_merge_result

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
