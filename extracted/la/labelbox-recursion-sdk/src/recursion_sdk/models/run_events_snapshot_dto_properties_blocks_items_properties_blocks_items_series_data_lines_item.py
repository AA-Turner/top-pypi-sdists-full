from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.run_events_snapshot_dto_properties_blocks_items_properties_blocks_items_series_data_lines_item_points_item import RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsSeriesDataLinesItemPointsItem





T = TypeVar("T", bound="RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsSeriesDataLinesItem")



@_attrs_define
class RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsSeriesDataLinesItem:
    """ One named line within a series block, e.g. one metric or one group of a stacked area.

        Attributes:
            key (str): Stable series key used to match the line across steps.
            label (str): Human-readable line label shown in the legend.
            points (list[RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsSeriesDataLinesItemPointsItem]): This
                step's incremental points for the line.
            group (None | str | Unset): Optional group id for stacking or shared styling.
     """

    key: str
    label: str
    points: list[RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsSeriesDataLinesItemPointsItem]
    group: None | str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.run_events_snapshot_dto_properties_blocks_items_properties_blocks_items_series_data_lines_item_points_item import RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsSeriesDataLinesItemPointsItem # noqa: PLC0415
        key = self.key

        label = self.label

        points = []
        for points_item_data in self.points:
            points_item = points_item_data.to_dict()
            points.append(points_item)



        group: None | str | Unset
        if isinstance(self.group, Unset):
            group = UNSET
        else:
            group = self.group


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "key": key,
            "label": label,
            "points": points,
        })
        if group is not UNSET:
            field_dict["group"] = group

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.run_events_snapshot_dto_properties_blocks_items_properties_blocks_items_series_data_lines_item_points_item import RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsSeriesDataLinesItemPointsItem # noqa: PLC0415
        d = dict(src_dict)
        key = d.pop("key")

        label = d.pop("label")

        points = []
        _points = d.pop("points")
        for points_item_data in (_points):
            points_item = RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsSeriesDataLinesItemPointsItem.from_dict(points_item_data)



            points.append(points_item)


        def _parse_group(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        group = _parse_group(d.pop("group", UNSET))


        run_events_snapshot_dto_properties_blocks_items_properties_blocks_items_series_data_lines_item = cls(
            key=key,
            label=label,
            points=points,
            group=group,
        )

        return run_events_snapshot_dto_properties_blocks_items_properties_blocks_items_series_data_lines_item

