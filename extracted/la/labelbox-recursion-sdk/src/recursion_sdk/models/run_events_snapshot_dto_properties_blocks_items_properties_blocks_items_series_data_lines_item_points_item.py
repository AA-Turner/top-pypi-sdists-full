from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast






T = TypeVar("T", bound="RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsSeriesDataLinesItemPointsItem")



@_attrs_define
class RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsSeriesDataLinesItemPointsItem:
    """ One point of a series line; y is null where the trainer has no value for that x.

        Attributes:
            x (float): X coordinate (step index or timestamp, per the block axis).
            y (float | None): Y value at this x, or null where the trainer has none.
     """

    x: float
    y: float | None





    def to_dict(self) -> dict[str, Any]:
        x = self.x

        y: float | None
        y = self.y


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "x": x,
            "y": y,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        x = d.pop("x")

        def _parse_y(data: object) -> float | None:
            if data is None:
                return data
            return cast(float | None, data)

        y = _parse_y(d.pop("y"))


        run_events_snapshot_dto_properties_blocks_items_properties_blocks_items_series_data_lines_item_points_item = cls(
            x=x,
            y=y,
        )

        return run_events_snapshot_dto_properties_blocks_items_properties_blocks_items_series_data_lines_item_points_item

