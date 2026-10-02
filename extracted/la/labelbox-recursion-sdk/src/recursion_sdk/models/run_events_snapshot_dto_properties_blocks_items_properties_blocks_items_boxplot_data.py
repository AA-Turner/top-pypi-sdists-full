from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.run_events_snapshot_dto_properties_blocks_items_properties_blocks_items_boxplot_data_boxes_item import RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsBoxplotDataBoxesItem
  from ..models.run_events_snapshot_dto_properties_blocks_items_properties_blocks_items_boxplot_data_stats_item import RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsBoxplotDataStatsItem





T = TypeVar("T", bound="RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsBoxplotData")



@_attrs_define
class RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsBoxplotData:
    """ Boxplot payload: the boxes, accompanying stats, and raw group stds.

        Attributes:
            boxes (list[RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsBoxplotDataBoxesItem]): Precomputed
                Tukey boxes rendered side by side.
            stats (list[RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsBoxplotDataStatsItem]): Labeled
                scalars shown alongside the boxes.
            group_stds (list[float]): Raw per-group standard deviations, retained for server-side pooling.
     """

    boxes: list[RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsBoxplotDataBoxesItem]
    stats: list[RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsBoxplotDataStatsItem]
    group_stds: list[float]





    def to_dict(self) -> dict[str, Any]:
        from ..models.run_events_snapshot_dto_properties_blocks_items_properties_blocks_items_boxplot_data_boxes_item import RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsBoxplotDataBoxesItem # noqa: PLC0415
        from ..models.run_events_snapshot_dto_properties_blocks_items_properties_blocks_items_boxplot_data_stats_item import RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsBoxplotDataStatsItem # noqa: PLC0415
        boxes = []
        for boxes_item_data in self.boxes:
            boxes_item = boxes_item_data.to_dict()
            boxes.append(boxes_item)



        stats = []
        for stats_item_data in self.stats:
            stats_item = stats_item_data.to_dict()
            stats.append(stats_item)



        group_stds = self.group_stds




        field_dict: dict[str, Any] = {}

        field_dict.update({
            "boxes": boxes,
            "stats": stats,
            "group_stds": group_stds,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.run_events_snapshot_dto_properties_blocks_items_properties_blocks_items_boxplot_data_boxes_item import RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsBoxplotDataBoxesItem # noqa: PLC0415
        from ..models.run_events_snapshot_dto_properties_blocks_items_properties_blocks_items_boxplot_data_stats_item import RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsBoxplotDataStatsItem # noqa: PLC0415
        d = dict(src_dict)
        boxes = []
        _boxes = d.pop("boxes")
        for boxes_item_data in (_boxes):
            boxes_item = RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsBoxplotDataBoxesItem.from_dict(boxes_item_data)



            boxes.append(boxes_item)


        stats = []
        _stats = d.pop("stats")
        for stats_item_data in (_stats):
            stats_item = RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsBoxplotDataStatsItem.from_dict(stats_item_data)



            stats.append(stats_item)


        group_stds = cast(list[float], d.pop("group_stds"))


        run_events_snapshot_dto_properties_blocks_items_properties_blocks_items_boxplot_data = cls(
            boxes=boxes,
            stats=stats,
            group_stds=group_stds,
        )

        return run_events_snapshot_dto_properties_blocks_items_properties_blocks_items_boxplot_data

