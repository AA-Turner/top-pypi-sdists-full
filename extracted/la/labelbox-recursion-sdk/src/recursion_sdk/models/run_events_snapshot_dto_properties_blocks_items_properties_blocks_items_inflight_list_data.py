from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.run_events_snapshot_dto_properties_blocks_items_properties_blocks_items_inflight_list_data_per_rollout_item import RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsInflightListDataPerRolloutItem





T = TypeVar("T", bound="RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsInflightListData")



@_attrs_define
class RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsInflightListData:
    """ Inflight-list payload: the in-progress rollouts and their live progress.

        Attributes:
            total (int): Total in-flight rollouts represented.
            per_rollout
                (list[RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsInflightListDataPerRolloutItem]): Per-
                rollout progress entries for the in-flight list.
     """

    total: int
    per_rollout: list[RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsInflightListDataPerRolloutItem]





    def to_dict(self) -> dict[str, Any]:
        from ..models.run_events_snapshot_dto_properties_blocks_items_properties_blocks_items_inflight_list_data_per_rollout_item import RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsInflightListDataPerRolloutItem # noqa: PLC0415
        total = self.total

        per_rollout = []
        for per_rollout_item_data in self.per_rollout:
            per_rollout_item = per_rollout_item_data.to_dict()
            per_rollout.append(per_rollout_item)




        field_dict: dict[str, Any] = {}

        field_dict.update({
            "total": total,
            "per_rollout": per_rollout,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.run_events_snapshot_dto_properties_blocks_items_properties_blocks_items_inflight_list_data_per_rollout_item import RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsInflightListDataPerRolloutItem # noqa: PLC0415
        d = dict(src_dict)
        total = d.pop("total")

        per_rollout = []
        _per_rollout = d.pop("per_rollout")
        for per_rollout_item_data in (_per_rollout):
            per_rollout_item = RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsInflightListDataPerRolloutItem.from_dict(per_rollout_item_data)



            per_rollout.append(per_rollout_item)


        run_events_snapshot_dto_properties_blocks_items_properties_blocks_items_inflight_list_data = cls(
            total=total,
            per_rollout=per_rollout,
        )

        return run_events_snapshot_dto_properties_blocks_items_properties_blocks_items_inflight_list_data

