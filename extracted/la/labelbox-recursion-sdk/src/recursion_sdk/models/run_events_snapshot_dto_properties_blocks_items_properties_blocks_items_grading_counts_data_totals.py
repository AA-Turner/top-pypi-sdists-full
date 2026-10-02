from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsGradingCountsDataTotals")



@_attrs_define
class RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsGradingCountsDataTotals:
    """ Grading-progress totals: in-flight/complete/failed grader-row counts.

        Attributes:
            in_flight (int): Grader rows currently being graded.
            complete (int): Grader rows that finished grading.
            failed (int): Grader rows that failed grading.
     """

    in_flight: int
    complete: int
    failed: int





    def to_dict(self) -> dict[str, Any]:
        in_flight = self.in_flight

        complete = self.complete

        failed = self.failed


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "in_flight": in_flight,
            "complete": complete,
            "failed": failed,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        in_flight = d.pop("in_flight")

        complete = d.pop("complete")

        failed = d.pop("failed")

        run_events_snapshot_dto_properties_blocks_items_properties_blocks_items_grading_counts_data_totals = cls(
            in_flight=in_flight,
            complete=complete,
            failed=failed,
        )

        return run_events_snapshot_dto_properties_blocks_items_properties_blocks_items_grading_counts_data_totals

