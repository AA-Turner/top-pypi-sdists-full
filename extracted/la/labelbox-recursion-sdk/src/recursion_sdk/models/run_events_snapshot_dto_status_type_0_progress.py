from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast






T = TypeVar("T", bound="RunEventsSnapshotDtoStatusType0Progress")



@_attrs_define
class RunEventsSnapshotDtoStatusType0Progress:
    """ Count-based (done/expected) OR step-based (step/total_steps); a job fills whichever axis it has.

        Attributes:
            done (int | None | Unset): Units completed so far on the count-based axis.
            expected (int | None | Unset): Total units expected on the count-based axis.
            in_flight (int | None | Unset): Units currently in flight on the count-based axis.
            pending (int | None | Unset): Units not yet started on the count-based axis.
            step (int | None | Unset): Current step index on the step-based axis.
            total_steps (int | None | Unset): Total planned steps on the step-based axis.
            pct (float | None | Unset): Fraction complete in [0, 1], when the job reports one.
     """

    done: int | None | Unset = UNSET
    expected: int | None | Unset = UNSET
    in_flight: int | None | Unset = UNSET
    pending: int | None | Unset = UNSET
    step: int | None | Unset = UNSET
    total_steps: int | None | Unset = UNSET
    pct: float | None | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        done: int | None | Unset
        if isinstance(self.done, Unset):
            done = UNSET
        else:
            done = self.done

        expected: int | None | Unset
        if isinstance(self.expected, Unset):
            expected = UNSET
        else:
            expected = self.expected

        in_flight: int | None | Unset
        if isinstance(self.in_flight, Unset):
            in_flight = UNSET
        else:
            in_flight = self.in_flight

        pending: int | None | Unset
        if isinstance(self.pending, Unset):
            pending = UNSET
        else:
            pending = self.pending

        step: int | None | Unset
        if isinstance(self.step, Unset):
            step = UNSET
        else:
            step = self.step

        total_steps: int | None | Unset
        if isinstance(self.total_steps, Unset):
            total_steps = UNSET
        else:
            total_steps = self.total_steps

        pct: float | None | Unset
        if isinstance(self.pct, Unset):
            pct = UNSET
        else:
            pct = self.pct


        field_dict: dict[str, Any] = {}

        field_dict.update({
        })
        if done is not UNSET:
            field_dict["done"] = done
        if expected is not UNSET:
            field_dict["expected"] = expected
        if in_flight is not UNSET:
            field_dict["in_flight"] = in_flight
        if pending is not UNSET:
            field_dict["pending"] = pending
        if step is not UNSET:
            field_dict["step"] = step
        if total_steps is not UNSET:
            field_dict["total_steps"] = total_steps
        if pct is not UNSET:
            field_dict["pct"] = pct

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        def _parse_done(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        done = _parse_done(d.pop("done", UNSET))


        def _parse_expected(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        expected = _parse_expected(d.pop("expected", UNSET))


        def _parse_in_flight(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        in_flight = _parse_in_flight(d.pop("in_flight", UNSET))


        def _parse_pending(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        pending = _parse_pending(d.pop("pending", UNSET))


        def _parse_step(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        step = _parse_step(d.pop("step", UNSET))


        def _parse_total_steps(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        total_steps = _parse_total_steps(d.pop("total_steps", UNSET))


        def _parse_pct(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        pct = _parse_pct(d.pop("pct", UNSET))


        run_events_snapshot_dto_status_type_0_progress = cls(
            done=done,
            expected=expected,
            in_flight=in_flight,
            pending=pending,
            step=step,
            total_steps=total_steps,
            pct=pct,
        )

        return run_events_snapshot_dto_status_type_0_progress

