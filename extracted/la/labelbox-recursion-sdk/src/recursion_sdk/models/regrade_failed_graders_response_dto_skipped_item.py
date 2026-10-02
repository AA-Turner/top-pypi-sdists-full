from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from uuid import UUID






T = TypeVar("T", bound="RegradeFailedGradersResponseDtoSkippedItem")



@_attrs_define
class RegradeFailedGradersResponseDtoSkippedItem:
    """ A single problem run that qualified for re-grade but was not enqueued.

        Attributes:
            problem_run_id (UUID): The problem run that was skipped.
            reason (str): Why the run was skipped rather than re-graded.
     """

    problem_run_id: UUID
    reason: str





    def to_dict(self) -> dict[str, Any]:
        problem_run_id = str(self.problem_run_id)

        reason = self.reason


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "problemRunId": problem_run_id,
            "reason": reason,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        problem_run_id = UUID(d.pop("problemRunId"))




        reason = d.pop("reason")

        regrade_failed_graders_response_dto_skipped_item = cls(
            problem_run_id=problem_run_id,
            reason=reason,
        )

        return regrade_failed_graders_response_dto_skipped_item

