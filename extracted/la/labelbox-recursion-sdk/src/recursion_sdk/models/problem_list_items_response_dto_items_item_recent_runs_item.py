from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.problem_list_items_response_dto_items_item_recent_runs_item_status import ProblemListItemsResponseDtoItemsItemRecentRunsItemStatus
from typing import cast
from uuid import UUID






T = TypeVar("T", bound="ProblemListItemsResponseDtoItemsItemRecentRunsItem")



@_attrs_define
class ProblemListItemsResponseDtoItemsItemRecentRunsItem:
    """ Compact recent-run record used to render the per-problem sparkline.

        Attributes:
            id (UUID): Stable problem-run identifier (UUID). One solver attempt at one problem version.
            attempt_number (int): Sequential attempt number for this run within its problem (1-indexed). Example: 3.
            run_name (None | str): User-supplied display name for the run. Null for unnamed runs such as Taiga imports and
                interactive single runs.
            status (ProblemListItemsResponseDtoItemsItemRecentRunsItemStatus): Lifecycle status of the run.
            score (float | None): Final grader score for the run. Null when the run has not been graded.
     """

    id: UUID
    attempt_number: int
    run_name: None | str
    status: ProblemListItemsResponseDtoItemsItemRecentRunsItemStatus
    score: float | None





    def to_dict(self) -> dict[str, Any]:
        id = str(self.id)

        attempt_number = self.attempt_number

        run_name: None | str
        run_name = self.run_name

        status = self.status.value

        score: float | None
        score = self.score


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "id": id,
            "attemptNumber": attempt_number,
            "runName": run_name,
            "status": status,
            "score": score,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = UUID(d.pop("id"))




        attempt_number = d.pop("attemptNumber")

        def _parse_run_name(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        run_name = _parse_run_name(d.pop("runName"))


        status = ProblemListItemsResponseDtoItemsItemRecentRunsItemStatus(d.pop("status"))




        def _parse_score(data: object) -> float | None:
            if data is None:
                return data
            return cast(float | None, data)

        score = _parse_score(d.pop("score"))


        problem_list_items_response_dto_items_item_recent_runs_item = cls(
            id=id,
            attempt_number=attempt_number,
            run_name=run_name,
            status=status,
            score=score,
        )

        return problem_list_items_response_dto_items_item_recent_runs_item

