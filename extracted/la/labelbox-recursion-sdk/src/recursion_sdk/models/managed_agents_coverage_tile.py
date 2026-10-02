from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.managed_agents_coverage_tile_history_status import ManagedAgentsCoverageTileHistoryStatus
from typing import cast






T = TypeVar("T", bound="ManagedAgentsCoverageTile")



@_attrs_define
class ManagedAgentsCoverageTile:
    """ Evaluation coverage over the immutable eligible-session cohort, with explicit unavailable history.

        Example:
            {'delta_pp': 1.5, 'eligible_session_count': 1, 'evaluated_eligible_session_count': 1,
                'evaluation_snapshot_count': 1, 'history_status': 'complete', 'prior_rate': 1, 'rate': 1}

        Attributes:
            delta_pp (float | None): Current coverage minus prior coverage in percentage points, or null when incomparable.
            eligible_session_count (int | None): Immutable eligible target cohort size, or null when history is unavailable.
            evaluated_eligible_session_count (int | None): Eligible cohort sessions with at least one evaluation, or null
                when history is unavailable.
            evaluation_snapshot_count (int): Exact immutable evaluation rows in the current window.
            history_status (ManagedAgentsCoverageTileHistoryStatus): Whether immutable cohort history fully covers both
                requested windows.
            prior_rate (float | None): Coverage rate for the adjacent prior window, or null when unavailable or empty.
            rate (float | None): Evaluated eligible sessions divided by eligible sessions, or null when unavailable or
                empty.
     """

    delta_pp: float | None
    eligible_session_count: int | None
    evaluated_eligible_session_count: int | None
    evaluation_snapshot_count: int
    history_status: ManagedAgentsCoverageTileHistoryStatus
    prior_rate: float | None
    rate: float | None





    def to_dict(self) -> dict[str, Any]:
        delta_pp: float | None
        delta_pp = self.delta_pp

        eligible_session_count: int | None
        eligible_session_count = self.eligible_session_count

        evaluated_eligible_session_count: int | None
        evaluated_eligible_session_count = self.evaluated_eligible_session_count

        evaluation_snapshot_count = self.evaluation_snapshot_count

        history_status = self.history_status.value

        prior_rate: float | None
        prior_rate = self.prior_rate

        rate: float | None
        rate = self.rate


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "delta_pp": delta_pp,
            "eligible_session_count": eligible_session_count,
            "evaluated_eligible_session_count": evaluated_eligible_session_count,
            "evaluation_snapshot_count": evaluation_snapshot_count,
            "history_status": history_status,
            "prior_rate": prior_rate,
            "rate": rate,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        def _parse_delta_pp(data: object) -> float | None:
            if data is None:
                return data
            return cast(float | None, data)

        delta_pp = _parse_delta_pp(d.pop("delta_pp"))


        def _parse_eligible_session_count(data: object) -> int | None:
            if data is None:
                return data
            return cast(int | None, data)

        eligible_session_count = _parse_eligible_session_count(d.pop("eligible_session_count"))


        def _parse_evaluated_eligible_session_count(data: object) -> int | None:
            if data is None:
                return data
            return cast(int | None, data)

        evaluated_eligible_session_count = _parse_evaluated_eligible_session_count(d.pop("evaluated_eligible_session_count"))


        evaluation_snapshot_count = d.pop("evaluation_snapshot_count")

        history_status = ManagedAgentsCoverageTileHistoryStatus(d.pop("history_status"))




        def _parse_prior_rate(data: object) -> float | None:
            if data is None:
                return data
            return cast(float | None, data)

        prior_rate = _parse_prior_rate(d.pop("prior_rate"))


        def _parse_rate(data: object) -> float | None:
            if data is None:
                return data
            return cast(float | None, data)

        rate = _parse_rate(d.pop("rate"))


        managed_agents_coverage_tile = cls(
            delta_pp=delta_pp,
            eligible_session_count=eligible_session_count,
            evaluated_eligible_session_count=evaluated_eligible_session_count,
            evaluation_snapshot_count=evaluation_snapshot_count,
            history_status=history_status,
            prior_rate=prior_rate,
            rate=rate,
        )

        return managed_agents_coverage_tile

