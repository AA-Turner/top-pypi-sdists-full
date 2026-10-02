from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast






T = TypeVar("T", bound="RunEventsSnapshotDtoStatusType0Throughput")



@_attrs_define
class RunEventsSnapshotDtoStatusType0Throughput:
    """ Rollout throughput snapshot at status-report time.

        Attributes:
            concurrency (int | None | Unset): Rollouts running concurrently at report time.
            max_concurrency (int | None | Unset): Configured ceiling on concurrent rollouts.
            tokens_per_s (float | None | Unset): Token generation rate across active rollouts.
            units_per_s (float | None | Unset): Completed-units rate (rollouts or steps per second).
     """

    concurrency: int | None | Unset = UNSET
    max_concurrency: int | None | Unset = UNSET
    tokens_per_s: float | None | Unset = UNSET
    units_per_s: float | None | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        concurrency: int | None | Unset
        if isinstance(self.concurrency, Unset):
            concurrency = UNSET
        else:
            concurrency = self.concurrency

        max_concurrency: int | None | Unset
        if isinstance(self.max_concurrency, Unset):
            max_concurrency = UNSET
        else:
            max_concurrency = self.max_concurrency

        tokens_per_s: float | None | Unset
        if isinstance(self.tokens_per_s, Unset):
            tokens_per_s = UNSET
        else:
            tokens_per_s = self.tokens_per_s

        units_per_s: float | None | Unset
        if isinstance(self.units_per_s, Unset):
            units_per_s = UNSET
        else:
            units_per_s = self.units_per_s


        field_dict: dict[str, Any] = {}

        field_dict.update({
        })
        if concurrency is not UNSET:
            field_dict["concurrency"] = concurrency
        if max_concurrency is not UNSET:
            field_dict["max_concurrency"] = max_concurrency
        if tokens_per_s is not UNSET:
            field_dict["tokens_per_s"] = tokens_per_s
        if units_per_s is not UNSET:
            field_dict["units_per_s"] = units_per_s

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        def _parse_concurrency(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        concurrency = _parse_concurrency(d.pop("concurrency", UNSET))


        def _parse_max_concurrency(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        max_concurrency = _parse_max_concurrency(d.pop("max_concurrency", UNSET))


        def _parse_tokens_per_s(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        tokens_per_s = _parse_tokens_per_s(d.pop("tokens_per_s", UNSET))


        def _parse_units_per_s(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        units_per_s = _parse_units_per_s(d.pop("units_per_s", UNSET))


        run_events_snapshot_dto_status_type_0_throughput = cls(
            concurrency=concurrency,
            max_concurrency=max_concurrency,
            tokens_per_s=tokens_per_s,
            units_per_s=units_per_s,
        )

        return run_events_snapshot_dto_status_type_0_throughput

