from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.run_events_snapshot_dto_properties_blocks_items_properties_blocks_items_grading_counts_type import RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsGradingCountsType
from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.run_events_snapshot_dto_properties_blocks_items_properties_blocks_items_grading_counts_data import RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsGradingCountsData





T = TypeVar("T", bound="RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsGradingCounts")



@_attrs_define
class RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsGradingCounts:
    """ Typed block rendered as grading-progress count tiles, e.g. from platform-launched or trainer-internal grader rows.

        Attributes:
            title (str): Trainer-authored title shown above the rendered block.
            type_ (RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsGradingCountsType): Block-type
                discriminant.
            data (RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsGradingCountsData): Grading-counts payload:
                overall totals plus a per-step breakdown.
            subtitle (None | str | Unset): Optional trainer-authored subtitle for the block.
     """

    title: str
    type_: RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsGradingCountsType
    data: RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsGradingCountsData
    subtitle: None | str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.run_events_snapshot_dto_properties_blocks_items_properties_blocks_items_grading_counts_data import RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsGradingCountsData # noqa: PLC0415
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
        from ..models.run_events_snapshot_dto_properties_blocks_items_properties_blocks_items_grading_counts_data import RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsGradingCountsData # noqa: PLC0415
        d = dict(src_dict)
        title = d.pop("title")

        type_ = RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsGradingCountsType(d.pop("type"))




        data = RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsGradingCountsData.from_dict(d.pop("data"))




        def _parse_subtitle(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        subtitle = _parse_subtitle(d.pop("subtitle", UNSET))


        run_events_snapshot_dto_properties_blocks_items_properties_blocks_items_grading_counts = cls(
            title=title,
            type_=type_,
            data=data,
            subtitle=subtitle,
        )

        return run_events_snapshot_dto_properties_blocks_items_properties_blocks_items_grading_counts

