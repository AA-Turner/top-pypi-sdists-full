from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast






T = TypeVar("T", bound="RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsGradingCountsDataByStepItem")



@_attrs_define
class RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsGradingCountsDataByStepItem:
    """ Grading-progress counts for one step (or null for the not-yet-stepped bucket).

        Attributes:
            step (int | None): Step these counts belong to, or null for the not-yet-stepped bucket.
            in_flight (int): Grader rows in flight for the step.
            complete (int): Grader rows completed for the step.
            failed (int): Grader rows failed for the step.
     """

    step: int | None
    in_flight: int
    complete: int
    failed: int





    def to_dict(self) -> dict[str, Any]:
        step: int | None
        step = self.step

        in_flight = self.in_flight

        complete = self.complete

        failed = self.failed


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "step": step,
            "in_flight": in_flight,
            "complete": complete,
            "failed": failed,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        def _parse_step(data: object) -> int | None:
            if data is None:
                return data
            return cast(int | None, data)

        step = _parse_step(d.pop("step"))


        in_flight = d.pop("in_flight")

        complete = d.pop("complete")

        failed = d.pop("failed")

        run_events_snapshot_dto_properties_blocks_items_properties_blocks_items_grading_counts_data_by_step_item = cls(
            step=step,
            in_flight=in_flight,
            complete=complete,
            failed=failed,
        )

        return run_events_snapshot_dto_properties_blocks_items_properties_blocks_items_grading_counts_data_by_step_item

