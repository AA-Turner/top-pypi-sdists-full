from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast






T = TypeVar("T", bound="RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsPillsDataHeader")



@_attrs_define
class RunEventsSnapshotDtoPropertiesBlocksItemsPropertiesBlocksItemsPillsDataHeader:
    """ Summary counts shown above a pills block, e.g. groups complete / target.

        Attributes:
            groups_complete (int): Groups that have reached their target rollout count.
            groups_target (int): Total groups targeted for this step.
            rollouts (int): Total rollouts collected across all groups.
            constant_groups (int): Groups whose rollouts all share one constant reward.
            carryover (int | None | Unset): Rollouts carried over from a prior step, when any.
     """

    groups_complete: int
    groups_target: int
    rollouts: int
    constant_groups: int
    carryover: int | None | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        groups_complete = self.groups_complete

        groups_target = self.groups_target

        rollouts = self.rollouts

        constant_groups = self.constant_groups

        carryover: int | None | Unset
        if isinstance(self.carryover, Unset):
            carryover = UNSET
        else:
            carryover = self.carryover


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "groups_complete": groups_complete,
            "groups_target": groups_target,
            "rollouts": rollouts,
            "constant_groups": constant_groups,
        })
        if carryover is not UNSET:
            field_dict["carryover"] = carryover

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        groups_complete = d.pop("groups_complete")

        groups_target = d.pop("groups_target")

        rollouts = d.pop("rollouts")

        constant_groups = d.pop("constant_groups")

        def _parse_carryover(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        carryover = _parse_carryover(d.pop("carryover", UNSET))


        run_events_snapshot_dto_properties_blocks_items_properties_blocks_items_pills_data_header = cls(
            groups_complete=groups_complete,
            groups_target=groups_target,
            rollouts=rollouts,
            constant_groups=constant_groups,
            carryover=carryover,
        )

        return run_events_snapshot_dto_properties_blocks_items_properties_blocks_items_pills_data_header

