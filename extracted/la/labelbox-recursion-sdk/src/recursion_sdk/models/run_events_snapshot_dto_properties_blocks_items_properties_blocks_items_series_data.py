from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.run_events_snapshot_dto_properties_blocks_items_properties_blocks_items_series_data_axis import RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsSeriesDataAxis
from typing import cast

if TYPE_CHECKING:
  from ..models.run_events_snapshot_dto_properties_blocks_items_properties_blocks_items_series_data_axes_item import RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsSeriesDataAxesItem
  from ..models.run_events_snapshot_dto_properties_blocks_items_properties_blocks_items_series_data_lines_item import RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsSeriesDataLinesItem





T = TypeVar("T", bound="RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsSeriesData")



@_attrs_define
class RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsSeriesData:
    """ Series payload: this step incremental line data plus axis hints.

        Attributes:
            axis (RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsSeriesDataAxis): Whether the x-axis is step
                index or wall-clock time. 'step': the platform concatenates this step's incremental points onto every prior
                step's for the same line key into one continuous cross-step trend chart -- each document must carry only THIS
                step's own new points, never replay history. 'time': the line stays scoped to this one step's own within-step
                curve and is never concatenated across steps (e.g. throughput sampled during the step).
            lines (list[RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsSeriesDataLinesItem]): Named lines
                composing this chart.
            present (bool): Whether this step contributed any points (vs a placeholder frame).
            axes (list[RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsSeriesDataAxesItem]): Per-series
                axis/mark hints, or an empty array when none were emitted.
     """

    axis: RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsSeriesDataAxis
    lines: list[RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsSeriesDataLinesItem]
    present: bool
    axes: list[RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsSeriesDataAxesItem]





    def to_dict(self) -> dict[str, Any]:
        from ..models.run_events_snapshot_dto_properties_blocks_items_properties_blocks_items_series_data_axes_item import RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsSeriesDataAxesItem # noqa: PLC0415
        from ..models.run_events_snapshot_dto_properties_blocks_items_properties_blocks_items_series_data_lines_item import RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsSeriesDataLinesItem # noqa: PLC0415
        axis = self.axis.value

        lines = []
        for lines_item_data in self.lines:
            lines_item = lines_item_data.to_dict()
            lines.append(lines_item)



        present = self.present

        axes = []
        for axes_item_data in self.axes:
            axes_item = axes_item_data.to_dict()
            axes.append(axes_item)




        field_dict: dict[str, Any] = {}

        field_dict.update({
            "axis": axis,
            "lines": lines,
            "present": present,
            "axes": axes,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.run_events_snapshot_dto_properties_blocks_items_properties_blocks_items_series_data_axes_item import RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsSeriesDataAxesItem # noqa: PLC0415
        from ..models.run_events_snapshot_dto_properties_blocks_items_properties_blocks_items_series_data_lines_item import RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsSeriesDataLinesItem # noqa: PLC0415
        d = dict(src_dict)
        axis = RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsSeriesDataAxis(d.pop("axis"))




        lines = []
        _lines = d.pop("lines")
        for lines_item_data in (_lines):
            lines_item = RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsSeriesDataLinesItem.from_dict(lines_item_data)



            lines.append(lines_item)


        present = d.pop("present")

        axes = []
        _axes = d.pop("axes")
        for axes_item_data in (_axes):
            axes_item = RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsSeriesDataAxesItem.from_dict(axes_item_data)



            axes.append(axes_item)


        run_events_snapshot_dto_properties_blocks_items_properties_blocks_items_series_data = cls(
            axis=axis,
            lines=lines,
            present=present,
            axes=axes,
        )

        return run_events_snapshot_dto_properties_blocks_items_properties_blocks_items_series_data

