from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.run_events_snapshot_dto_properties_blocks_items_properties_blocks_items_series_data_axes_item_kind_type_0 import RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsSeriesDataAxesItemKindType0
from ..models.run_events_snapshot_dto_properties_blocks_items_properties_blocks_items_series_data_axes_item_side import RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsSeriesDataAxesItemSide
from ..types import UNSET, Unset
from typing import cast






T = TypeVar("T", bound="RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsSeriesDataAxesItem")



@_attrs_define
class RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsSeriesDataAxesItem:
    """ Rendering hint for a dual-axis series chart (e.g. throughput overlaying a scatter).

        Attributes:
            key (str): Series key this axis hint applies to.
            side (RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsSeriesDataAxesItemSide): Which vertical axis
                the series is drawn against.
            kind (None | RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsSeriesDataAxesItemKindType0 | Unset):
                Optional mark style override for the series.
     """

    key: str
    side: RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsSeriesDataAxesItemSide
    kind: None | RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsSeriesDataAxesItemKindType0 | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        key = self.key

        side = self.side.value

        kind: None | str | Unset
        if isinstance(self.kind, Unset):
            kind = UNSET
        elif isinstance(self.kind, RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsSeriesDataAxesItemKindType0):
            kind = self.kind.value
        else:
            kind = self.kind


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "key": key,
            "side": side,
        })
        if kind is not UNSET:
            field_dict["kind"] = kind

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        key = d.pop("key")

        side = RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsSeriesDataAxesItemSide(d.pop("side"))




        def _parse_kind(data: object) -> None | RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsSeriesDataAxesItemKindType0 | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                kind_type_0 = RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsSeriesDataAxesItemKindType0(data)



                return kind_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsSeriesDataAxesItemKindType0 | Unset, data)

        kind = _parse_kind(d.pop("kind", UNSET))


        run_events_snapshot_dto_properties_blocks_items_properties_blocks_items_series_data_axes_item = cls(
            key=key,
            side=side,
            kind=kind,
        )

        return run_events_snapshot_dto_properties_blocks_items_properties_blocks_items_series_data_axes_item

