from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.run_events_snapshot_dto_properties_blocks_items_properties_blocks_items_histogram_type import RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsHistogramType
from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.run_events_snapshot_dto_properties_blocks_items_properties_blocks_items_histogram_data import RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsHistogramData





T = TypeVar("T", bound="RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsHistogram")



@_attrs_define
class RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsHistogram:
    """ Typed block rendered as a bar-chart histogram (e.g. step-scoped reward distribution). The distributions panel --
    emit one histogram block per step for maximum granularity; the platform pools/merges across steps itself, no cross-
    step aggregation logic belongs in the trainer.

        Attributes:
            title (str): Trainer-authored title shown above the rendered block.
            type_ (RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsHistogramType): Block-type discriminant.
            data (RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsHistogramData): Histogram payload: the
                precomputed bins.
            subtitle (None | str | Unset): Optional trainer-authored subtitle for the block.
     """

    title: str
    type_: RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsHistogramType
    data: RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsHistogramData
    subtitle: None | str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.run_events_snapshot_dto_properties_blocks_items_properties_blocks_items_histogram_data import RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsHistogramData # noqa: PLC0415
        title = self.title

        type_ = self.type_.value

        data = self.data.to_dict()

        subtitle: None | str | Unset
        if isinstance(self.subtitle, Unset):
            subtitle = UNSET
        else:
            subtitle = self.subtitle


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "title": title,
            "type": type_,
            "data": data,
        })
        if subtitle is not UNSET:
            field_dict["subtitle"] = subtitle

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.run_events_snapshot_dto_properties_blocks_items_properties_blocks_items_histogram_data import RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsHistogramData # noqa: PLC0415
        d = dict(src_dict)
        title = d.pop("title")

        type_ = RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsHistogramType(d.pop("type"))




        data = RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsHistogramData.from_dict(d.pop("data"))




        def _parse_subtitle(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        subtitle = _parse_subtitle(d.pop("subtitle", UNSET))


        run_events_snapshot_dto_properties_blocks_items_properties_blocks_items_histogram = cls(
            title=title,
            type_=type_,
            data=data,
            subtitle=subtitle,
        )

        return run_events_snapshot_dto_properties_blocks_items_properties_blocks_items_histogram

