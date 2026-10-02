from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsHistogramDataBinsItem")



@_attrs_define
class RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsHistogramDataBinsItem:
    """ One bin of a reward histogram: half-open [lo, hi) range and its count.

        Attributes:
            lo (float): Inclusive lower edge of the bin range.
            hi (float): Exclusive upper edge of the bin range.
            count (int): Number of samples falling in this bin.
     """

    lo: float
    hi: float
    count: int





    def to_dict(self) -> dict[str, Any]:
        lo = self.lo

        hi = self.hi

        count = self.count


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "lo": lo,
            "hi": hi,
            "count": count,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        lo = d.pop("lo")

        hi = d.pop("hi")

        count = d.pop("count")

        run_events_snapshot_dto_properties_blocks_items_properties_blocks_items_histogram_data_bins_item = cls(
            lo=lo,
            hi=hi,
            count=count,
        )

        return run_events_snapshot_dto_properties_blocks_items_properties_blocks_items_histogram_data_bins_item

