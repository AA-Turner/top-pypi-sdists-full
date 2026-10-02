from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.run_events_snapshot_dto_properties_blocks_items_properties_blocks_items_pills_data_groups_item import RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsPillsDataGroupsItem
  from ..models.run_events_snapshot_dto_properties_blocks_items_properties_blocks_items_pills_data_header import RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsPillsDataHeader





T = TypeVar("T", bound="RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsPillsData")



@_attrs_define
class RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsPillsData:
    """ Pills payload: the summary header and per-group rollout pips.

        Attributes:
            header (RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsPillsDataHeader): Summary counts shown
                above a pills block, e.g. groups complete / target.
            groups (list[RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsPillsDataGroupsItem]): Per-task
                groups rendered as rollout pips.
     """

    header: RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsPillsDataHeader
    groups: list[RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsPillsDataGroupsItem]





    def to_dict(self) -> dict[str, Any]:
        from ..models.run_events_snapshot_dto_properties_blocks_items_properties_blocks_items_pills_data_groups_item import RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsPillsDataGroupsItem # noqa: PLC0415
        from ..models.run_events_snapshot_dto_properties_blocks_items_properties_blocks_items_pills_data_header import RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsPillsDataHeader # noqa: PLC0415
        header = self.header.to_dict()

        groups = []
        for groups_item_data in self.groups:
            groups_item = groups_item_data.to_dict()
            groups.append(groups_item)




        field_dict: dict[str, Any] = {}

        field_dict.update({
            "header": header,
            "groups": groups,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.run_events_snapshot_dto_properties_blocks_items_properties_blocks_items_pills_data_groups_item import RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsPillsDataGroupsItem # noqa: PLC0415
        from ..models.run_events_snapshot_dto_properties_blocks_items_properties_blocks_items_pills_data_header import RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsPillsDataHeader # noqa: PLC0415
        d = dict(src_dict)
        header = RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsPillsDataHeader.from_dict(d.pop("header"))




        groups = []
        _groups = d.pop("groups")
        for groups_item_data in (_groups):
            groups_item = RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsPillsDataGroupsItem.from_dict(groups_item_data)



            groups.append(groups_item)


        run_events_snapshot_dto_properties_blocks_items_properties_blocks_items_pills_data = cls(
            header=header,
            groups=groups,
        )

        return run_events_snapshot_dto_properties_blocks_items_properties_blocks_items_pills_data

