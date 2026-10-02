from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.run_events_snapshot_dto_properties_blocks_items_properties_blocks_items_pills_data_groups_item_slots_item import RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsPillsDataGroupsItemSlotsItem





T = TypeVar("T", bound="RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsPillsDataGroupsItem")



@_attrs_define
class RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsPillsDataGroupsItem:
    """ One task group within a pills block, with its slots and reward summary stats.

        Attributes:
            task_id (str): Task identifier this group of rollouts belongs to.
            slots (list[RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsPillsDataGroupsItemSlotsItem]): Per-
                rollout slots for the group.
            n (int): Rollouts collected for the group so far.
            target (int): Target rollout count for the group.
            mean (float | None | Unset): Mean reward across the group rollouts.
            std (float | None | Unset): Standard deviation of reward across the group.
            min_ (float | None | Unset): Minimum reward observed in the group.
            max_ (float | None | Unset): Maximum reward observed in the group.
     """

    task_id: str
    slots: list[RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsPillsDataGroupsItemSlotsItem]
    n: int
    target: int
    mean: float | None | Unset = UNSET
    std: float | None | Unset = UNSET
    min_: float | None | Unset = UNSET
    max_: float | None | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.run_events_snapshot_dto_properties_blocks_items_properties_blocks_items_pills_data_groups_item_slots_item import RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsPillsDataGroupsItemSlotsItem # noqa: PLC0415
        task_id = self.task_id

        slots = []
        for slots_item_data in self.slots:
            slots_item = slots_item_data.to_dict()
            slots.append(slots_item)



        n = self.n

        target = self.target

        mean: float | None | Unset
        if isinstance(self.mean, Unset):
            mean = UNSET
        else:
            mean = self.mean

        std: float | None | Unset
        if isinstance(self.std, Unset):
            std = UNSET
        else:
            std = self.std

        min_: float | None | Unset
        if isinstance(self.min_, Unset):
            min_ = UNSET
        else:
            min_ = self.min_

        max_: float | None | Unset
        if isinstance(self.max_, Unset):
            max_ = UNSET
        else:
            max_ = self.max_


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "task_id": task_id,
            "slots": slots,
            "n": n,
            "target": target,
        })
        if mean is not UNSET:
            field_dict["mean"] = mean
        if std is not UNSET:
            field_dict["std"] = std
        if min_ is not UNSET:
            field_dict["min"] = min_
        if max_ is not UNSET:
            field_dict["max"] = max_

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.run_events_snapshot_dto_properties_blocks_items_properties_blocks_items_pills_data_groups_item_slots_item import RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsPillsDataGroupsItemSlotsItem # noqa: PLC0415
        d = dict(src_dict)
        task_id = d.pop("task_id")

        slots = []
        _slots = d.pop("slots")
        for slots_item_data in (_slots):
            slots_item = RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsPillsDataGroupsItemSlotsItem.from_dict(slots_item_data)



            slots.append(slots_item)


        n = d.pop("n")

        target = d.pop("target")

        def _parse_mean(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        mean = _parse_mean(d.pop("mean", UNSET))


        def _parse_std(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        std = _parse_std(d.pop("std", UNSET))


        def _parse_min_(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        min_ = _parse_min_(d.pop("min", UNSET))


        def _parse_max_(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        max_ = _parse_max_(d.pop("max", UNSET))


        run_events_snapshot_dto_properties_blocks_items_properties_blocks_items_pills_data_groups_item = cls(
            task_id=task_id,
            slots=slots,
            n=n,
            target=target,
            mean=mean,
            std=std,
            min_=min_,
            max_=max_,
        )

        return run_events_snapshot_dto_properties_blocks_items_properties_blocks_items_pills_data_groups_item

