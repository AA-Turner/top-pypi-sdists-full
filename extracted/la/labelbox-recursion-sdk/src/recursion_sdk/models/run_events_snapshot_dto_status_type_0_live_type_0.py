from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.run_events_snapshot_dto_status_type_0_live_type_0_per_rollout_item import RunEventsSnapshotDtoStatusType0LiveType0PerRolloutItem





T = TypeVar("T", bound="RunEventsSnapshotDtoStatusType0LiveType0")



@_attrs_define
class RunEventsSnapshotDtoStatusType0LiveType0:
    """ Bounded, cheap, always-on live rollout telemetry (LT1-LT3). per_rollout_dropped is never silently truncated -- a
    real count is always reported. Renders the live-rollouts panel directly from the status envelope -- one of the two
    live-rollout-progress paths the dashboard renders (the other is the inflight-list block type); a trainer only needs
    one, not both, for the same rollouts.

        Attributes:
            in_flight (int): Rollouts currently in flight.
            total (int): Total rollouts tracked in this live window.
            running (int): Rollouts actively running right now.
            completed (int): Rollouts that have finished successfully.
            failed (int): Rollouts that have failed.
            cancelled (int): Rollouts that were cancelled.
            per_rollout_dropped (int): Count of in-flight rollouts omitted from the per_rollout sample.
            last_heartbeat_age_s (float | None | Unset): Seconds since the most recent live heartbeat across all rollouts.
            per_rollout (list[RunEventsSnapshotDtoStatusType0LiveType0PerRolloutItem] | Unset): Bounded per-rollout progress
                sample (a subset when many are in flight).
     """

    in_flight: int
    total: int
    running: int
    completed: int
    failed: int
    cancelled: int
    per_rollout_dropped: int
    last_heartbeat_age_s: float | None | Unset = UNSET
    per_rollout: list[RunEventsSnapshotDtoStatusType0LiveType0PerRolloutItem] | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.run_events_snapshot_dto_status_type_0_live_type_0_per_rollout_item import RunEventsSnapshotDtoStatusType0LiveType0PerRolloutItem # noqa: PLC0415
        in_flight = self.in_flight

        total = self.total

        running = self.running

        completed = self.completed

        failed = self.failed

        cancelled = self.cancelled

        per_rollout_dropped = self.per_rollout_dropped

        last_heartbeat_age_s: float | None | Unset
        if isinstance(self.last_heartbeat_age_s, Unset):
            last_heartbeat_age_s = UNSET
        else:
            last_heartbeat_age_s = self.last_heartbeat_age_s

        per_rollout: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.per_rollout, Unset):
            per_rollout = []
            for per_rollout_item_data in self.per_rollout:
                per_rollout_item = per_rollout_item_data.to_dict()
                per_rollout.append(per_rollout_item)




        field_dict: dict[str, Any] = {}

        field_dict.update({
            "in_flight": in_flight,
            "total": total,
            "running": running,
            "completed": completed,
            "failed": failed,
            "cancelled": cancelled,
            "per_rollout_dropped": per_rollout_dropped,
        })
        if last_heartbeat_age_s is not UNSET:
            field_dict["last_heartbeat_age_s"] = last_heartbeat_age_s
        if per_rollout is not UNSET:
            field_dict["per_rollout"] = per_rollout

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.run_events_snapshot_dto_status_type_0_live_type_0_per_rollout_item import RunEventsSnapshotDtoStatusType0LiveType0PerRolloutItem # noqa: PLC0415
        d = dict(src_dict)
        in_flight = d.pop("in_flight")

        total = d.pop("total")

        running = d.pop("running")

        completed = d.pop("completed")

        failed = d.pop("failed")

        cancelled = d.pop("cancelled")

        per_rollout_dropped = d.pop("per_rollout_dropped")

        def _parse_last_heartbeat_age_s(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        last_heartbeat_age_s = _parse_last_heartbeat_age_s(d.pop("last_heartbeat_age_s", UNSET))


        _per_rollout = d.pop("per_rollout", UNSET)
        per_rollout: list[RunEventsSnapshotDtoStatusType0LiveType0PerRolloutItem] | Unset = UNSET
        if _per_rollout is not UNSET:
            per_rollout = []
            for per_rollout_item_data in _per_rollout:
                per_rollout_item = RunEventsSnapshotDtoStatusType0LiveType0PerRolloutItem.from_dict(per_rollout_item_data)



                per_rollout.append(per_rollout_item)


        run_events_snapshot_dto_status_type_0_live_type_0 = cls(
            in_flight=in_flight,
            total=total,
            running=running,
            completed=completed,
            failed=failed,
            cancelled=cancelled,
            per_rollout_dropped=per_rollout_dropped,
            last_heartbeat_age_s=last_heartbeat_age_s,
            per_rollout=per_rollout,
        )

        return run_events_snapshot_dto_status_type_0_live_type_0

