from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsBoxplotDataStatsItem")



@_attrs_define
class RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsBoxplotDataStatsItem:
    """ One labeled scalar accompanying a boxplot block, e.g. a flat-group fraction.

        Attributes:
            label (str): Caption for the accompanying scalar.
            value (float): Scalar value shown alongside the boxes.
     """

    label: str
    value: float





    def to_dict(self) -> dict[str, Any]:
        label = self.label

        value = self.value


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "label": label,
            "value": value,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        label = d.pop("label")

        value = d.pop("value")

        run_events_snapshot_dto_properties_blocks_items_properties_blocks_items_boxplot_data_stats_item = cls(
            label=label,
            value=value,
        )

        return run_events_snapshot_dto_properties_blocks_items_properties_blocks_items_boxplot_data_stats_item

