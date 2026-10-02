from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.run_events_snapshot_dto_properties_blocks_items_properties_blocks_items_histogram_data_bins_item import RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsHistogramDataBinsItem





T = TypeVar("T", bound="RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsHistogramData")



@_attrs_define
class RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsHistogramData:
    """ Histogram payload: the precomputed bins.

        Attributes:
            bins (list[RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsHistogramDataBinsItem]): Contiguous
                histogram bins, low to high.
     """

    bins: list[RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsHistogramDataBinsItem]





    def to_dict(self) -> dict[str, Any]:
        from ..models.run_events_snapshot_dto_properties_blocks_items_properties_blocks_items_histogram_data_bins_item import RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsHistogramDataBinsItem # noqa: PLC0415
        bins = []
        for bins_item_data in self.bins:
            bins_item = bins_item_data.to_dict()
            bins.append(bins_item)




        field_dict: dict[str, Any] = {}

        field_dict.update({
            "bins": bins,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.run_events_snapshot_dto_properties_blocks_items_properties_blocks_items_histogram_data_bins_item import RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsHistogramDataBinsItem # noqa: PLC0415
        d = dict(src_dict)
        bins = []
        _bins = d.pop("bins")
        for bins_item_data in (_bins):
            bins_item = RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsHistogramDataBinsItem.from_dict(bins_item_data)



            bins.append(bins_item)


        run_events_snapshot_dto_properties_blocks_items_properties_blocks_items_histogram_data = cls(
            bins=bins,
        )

        return run_events_snapshot_dto_properties_blocks_items_properties_blocks_items_histogram_data

