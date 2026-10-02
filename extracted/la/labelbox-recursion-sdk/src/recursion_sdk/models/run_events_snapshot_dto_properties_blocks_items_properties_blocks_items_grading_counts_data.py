from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.run_events_snapshot_dto_properties_blocks_items_properties_blocks_items_grading_counts_data_by_step_item import RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsGradingCountsDataByStepItem
  from ..models.run_events_snapshot_dto_properties_blocks_items_properties_blocks_items_grading_counts_data_totals import RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsGradingCountsDataTotals





T = TypeVar("T", bound="RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsGradingCountsData")



@_attrs_define
class RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsGradingCountsData:
    """ Grading-counts payload: overall totals plus a per-step breakdown.

        Attributes:
            totals (RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsGradingCountsDataTotals): Grading-progress
                totals: in-flight/complete/failed grader-row counts.
            by_step (list[RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsGradingCountsDataByStepItem]):
                Grading counts broken down per step.
     """

    totals: RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsGradingCountsDataTotals
    by_step: list[RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsGradingCountsDataByStepItem]





    def to_dict(self) -> dict[str, Any]:
        from ..models.run_events_snapshot_dto_properties_blocks_items_properties_blocks_items_grading_counts_data_by_step_item import RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsGradingCountsDataByStepItem # noqa: PLC0415
        from ..models.run_events_snapshot_dto_properties_blocks_items_properties_blocks_items_grading_counts_data_totals import RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsGradingCountsDataTotals # noqa: PLC0415
        totals = self.totals.to_dict()

        by_step = []
        for by_step_item_data in self.by_step:
            by_step_item = by_step_item_data.to_dict()
            by_step.append(by_step_item)




        field_dict: dict[str, Any] = {}

        field_dict.update({
            "totals": totals,
            "by_step": by_step,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.run_events_snapshot_dto_properties_blocks_items_properties_blocks_items_grading_counts_data_by_step_item import RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsGradingCountsDataByStepItem # noqa: PLC0415
        from ..models.run_events_snapshot_dto_properties_blocks_items_properties_blocks_items_grading_counts_data_totals import RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsGradingCountsDataTotals # noqa: PLC0415
        d = dict(src_dict)
        totals = RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsGradingCountsDataTotals.from_dict(d.pop("totals"))




        by_step = []
        _by_step = d.pop("by_step")
        for by_step_item_data in (_by_step):
            by_step_item = RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsGradingCountsDataByStepItem.from_dict(by_step_item_data)



            by_step.append(by_step_item)


        run_events_snapshot_dto_properties_blocks_items_properties_blocks_items_grading_counts_data = cls(
            totals=totals,
            by_step=by_step,
        )

        return run_events_snapshot_dto_properties_blocks_items_properties_blocks_items_grading_counts_data

