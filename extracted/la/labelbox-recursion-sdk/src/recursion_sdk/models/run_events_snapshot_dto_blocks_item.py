from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.run_events_snapshot_dto_blocks_item_schema_version import RunEventsSnapshotDtoBlocksItemSchemaVersion
from typing import cast

if TYPE_CHECKING:
  from ..models.run_events_snapshot_dto_properties_blocks_items_properties_blocks_items_boxplot import RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsBoxplot
  from ..models.run_events_snapshot_dto_properties_blocks_items_properties_blocks_items_grading_counts import RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsGradingCounts
  from ..models.run_events_snapshot_dto_properties_blocks_items_properties_blocks_items_histogram import RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsHistogram
  from ..models.run_events_snapshot_dto_properties_blocks_items_properties_blocks_items_inflight_list import RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsInflightList
  from ..models.run_events_snapshot_dto_properties_blocks_items_properties_blocks_items_pills import RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsPills
  from ..models.run_events_snapshot_dto_properties_blocks_items_properties_blocks_items_scalar_tiles import RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsScalarTiles
  from ..models.run_events_snapshot_dto_properties_blocks_items_properties_blocks_items_series import RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsSeries
  from ..models.run_events_snapshot_dto_properties_blocks_items_properties_blocks_items_table_page import RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsTablePage





T = TypeVar("T", bound="RunEventsSnapshotDtoBlocksItem")



@_attrs_define
class RunEventsSnapshotDtoBlocksItem:
    """ 
        Attributes:
            schema_version (RunEventsSnapshotDtoBlocksItemSchemaVersion): Contract schema version of this blocks document.
            step (int): Trainer step this blocks document belongs to.
            frozen (bool): True when the step is final and its blocks are safe to cache indefinitely.
            blocks (list[RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsBoxplot |
                RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsGradingCounts |
                RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsHistogram |
                RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsInflightList |
                RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsPills |
                RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsScalarTiles |
                RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsSeries |
                RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsTablePage]): Typed telemetry blocks with read-side
                container normalization applied.
     """

    schema_version: RunEventsSnapshotDtoBlocksItemSchemaVersion
    step: int
    frozen: bool
    blocks: list[RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsBoxplot | RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsGradingCounts | RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsHistogram | RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsInflightList | RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsPills | RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsScalarTiles | RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsSeries | RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsTablePage]





    def to_dict(self) -> dict[str, Any]:
        from ..models.run_events_snapshot_dto_properties_blocks_items_properties_blocks_items_boxplot import RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsBoxplot # noqa: PLC0415
        from ..models.run_events_snapshot_dto_properties_blocks_items_properties_blocks_items_grading_counts import RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsGradingCounts # noqa: PLC0415
        from ..models.run_events_snapshot_dto_properties_blocks_items_properties_blocks_items_histogram import RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsHistogram # noqa: PLC0415
        from ..models.run_events_snapshot_dto_properties_blocks_items_properties_blocks_items_inflight_list import RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsInflightList # noqa: PLC0415
        from ..models.run_events_snapshot_dto_properties_blocks_items_properties_blocks_items_pills import RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsPills # noqa: PLC0415
        from ..models.run_events_snapshot_dto_properties_blocks_items_properties_blocks_items_scalar_tiles import RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsScalarTiles # noqa: PLC0415
        from ..models.run_events_snapshot_dto_properties_blocks_items_properties_blocks_items_series import RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsSeries # noqa: PLC0415
        from ..models.run_events_snapshot_dto_properties_blocks_items_properties_blocks_items_table_page import RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsTablePage # noqa: PLC0415
        schema_version = self.schema_version.value

        step = self.step

        frozen = self.frozen

        blocks = []
        for blocks_item_data in self.blocks:
            blocks_item: dict[str, Any]
            if isinstance(blocks_item_data, RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsScalarTiles):
                blocks_item = blocks_item_data.to_dict()
            elif isinstance(blocks_item_data, RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsSeries):
                blocks_item = blocks_item_data.to_dict()
            elif isinstance(blocks_item_data, RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsHistogram):
                blocks_item = blocks_item_data.to_dict()
            elif isinstance(blocks_item_data, RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsBoxplot):
                blocks_item = blocks_item_data.to_dict()
            elif isinstance(blocks_item_data, RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsPills):
                blocks_item = blocks_item_data.to_dict()
            elif isinstance(blocks_item_data, RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsGradingCounts):
                blocks_item = blocks_item_data.to_dict()
            elif isinstance(blocks_item_data, RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsTablePage):
                blocks_item = blocks_item_data.to_dict()
            else:
                blocks_item = blocks_item_data.to_dict()

            blocks.append(blocks_item)




        field_dict: dict[str, Any] = {}

        field_dict.update({
            "schema_version": schema_version,
            "step": step,
            "frozen": frozen,
            "blocks": blocks,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.run_events_snapshot_dto_properties_blocks_items_properties_blocks_items_boxplot import RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsBoxplot # noqa: PLC0415
        from ..models.run_events_snapshot_dto_properties_blocks_items_properties_blocks_items_grading_counts import RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsGradingCounts # noqa: PLC0415
        from ..models.run_events_snapshot_dto_properties_blocks_items_properties_blocks_items_histogram import RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsHistogram # noqa: PLC0415
        from ..models.run_events_snapshot_dto_properties_blocks_items_properties_blocks_items_inflight_list import RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsInflightList # noqa: PLC0415
        from ..models.run_events_snapshot_dto_properties_blocks_items_properties_blocks_items_pills import RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsPills # noqa: PLC0415
        from ..models.run_events_snapshot_dto_properties_blocks_items_properties_blocks_items_scalar_tiles import RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsScalarTiles # noqa: PLC0415
        from ..models.run_events_snapshot_dto_properties_blocks_items_properties_blocks_items_series import RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsSeries # noqa: PLC0415
        from ..models.run_events_snapshot_dto_properties_blocks_items_properties_blocks_items_table_page import RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsTablePage # noqa: PLC0415
        d = dict(src_dict)
        schema_version = RunEventsSnapshotDtoBlocksItemSchemaVersion(d.pop("schema_version"))




        step = d.pop("step")

        frozen = d.pop("frozen")

        blocks = []
        _blocks = d.pop("blocks")
        for blocks_item_data in (_blocks):
            def _parse_blocks_item(data: object) -> RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsBoxplot | RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsGradingCounts | RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsHistogram | RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsInflightList | RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsPills | RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsScalarTiles | RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsSeries | RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsTablePage:
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    blocks_item_type_0 = RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsScalarTiles.from_dict(data)



                    return blocks_item_type_0
                except (TypeError, ValueError, AttributeError, KeyError):
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    blocks_item_type_1 = RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsSeries.from_dict(data)



                    return blocks_item_type_1
                except (TypeError, ValueError, AttributeError, KeyError):
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    blocks_item_type_2 = RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsHistogram.from_dict(data)



                    return blocks_item_type_2
                except (TypeError, ValueError, AttributeError, KeyError):
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    blocks_item_type_3 = RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsBoxplot.from_dict(data)



                    return blocks_item_type_3
                except (TypeError, ValueError, AttributeError, KeyError):
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    blocks_item_type_4 = RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsPills.from_dict(data)



                    return blocks_item_type_4
                except (TypeError, ValueError, AttributeError, KeyError):
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    blocks_item_type_5 = RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsGradingCounts.from_dict(data)



                    return blocks_item_type_5
                except (TypeError, ValueError, AttributeError, KeyError):
                    pass
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    blocks_item_type_6 = RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsTablePage.from_dict(data)



                    return blocks_item_type_6
                except (TypeError, ValueError, AttributeError, KeyError):
                    pass
                if not isinstance(data, dict):
                    raise TypeError()
                blocks_item_type_7 = RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsInflightList.from_dict(data)



                return blocks_item_type_7

            blocks_item = _parse_blocks_item(blocks_item_data)

            blocks.append(blocks_item)


        run_events_snapshot_dto_blocks_item = cls(
            schema_version=schema_version,
            step=step,
            frozen=frozen,
            blocks=blocks,
        )

        return run_events_snapshot_dto_blocks_item

