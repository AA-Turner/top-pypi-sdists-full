from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast
from uuid import UUID






T = TypeVar("T", bound="ResetProblemResponseDto")



@_attrs_define
class ResetProblemResponseDto:
    """ Response payload for the problem-reset endpoint, summarising kept versions, deletions, and whether the problem was
    soft-deleted.

        Example:
            {'keptVersionIds': ['0c3ac467-57e1-4074-b57d-b6a7be392f71'], 'deletedCount': 4, 'problemSoftDeleted': False}

        Attributes:
            kept_version_ids (list[UUID]): Problem-version IDs retained after the reset (typically the imported baseline
                versions).
            deleted_count (int): Number of versions removed by the reset. Example: 4.
            problem_soft_deleted (bool): True when the reset removed every version and the problem itself was soft-deleted
                as a result.
     """

    kept_version_ids: list[UUID]
    deleted_count: int
    problem_soft_deleted: bool





    def to_dict(self) -> dict[str, Any]:
        kept_version_ids = []
        for kept_version_ids_item_data in self.kept_version_ids:
            kept_version_ids_item = str(kept_version_ids_item_data)
            kept_version_ids.append(kept_version_ids_item)



        deleted_count = self.deleted_count

        problem_soft_deleted = self.problem_soft_deleted


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "keptVersionIds": kept_version_ids,
            "deletedCount": deleted_count,
            "problemSoftDeleted": problem_soft_deleted,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        kept_version_ids = []
        _kept_version_ids = d.pop("keptVersionIds")
        for kept_version_ids_item_data in (_kept_version_ids):
            kept_version_ids_item = UUID(kept_version_ids_item_data)



            kept_version_ids.append(kept_version_ids_item)


        deleted_count = d.pop("deletedCount")

        problem_soft_deleted = d.pop("problemSoftDeleted")

        reset_problem_response_dto = cls(
            kept_version_ids=kept_version_ids,
            deleted_count=deleted_count,
            problem_soft_deleted=problem_soft_deleted,
        )

        return reset_problem_response_dto

