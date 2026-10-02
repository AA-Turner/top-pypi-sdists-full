from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast
from uuid import UUID






T = TypeVar("T", bound="UserEfficiencyResponseDtoRowsItem")



@_attrs_define
class UserEfficiencyResponseDtoRowsItem:
    """ Per-user efficiency aggregates summarising run count, scoring, and spend.

        Attributes:
            user_id (UUID): Stable user identifier (UUID).
            user_name (str): Display name of the user at the time the row was computed.
            total_runs (int): Total number of problem runs the user has executed.
            avg_score (float | None): Average rubric score across the user’s runs. Null when no scored runs exist.
            total_cost_usd (float | None): Total USD spend across the user’s runs. Null when no priced runs exist. Example:
                12.34.
            avg_cost_per_run (float | None): Average USD spend per run for the user. Null when no priced runs exist.
                Example: 0.42.
            avg_cost_per_problem (float | None): Average USD spend per distinct problem the user has attempted. Null when no
                priced runs exist. Example: 1.08.
     """

    user_id: UUID
    user_name: str
    total_runs: int
    avg_score: float | None
    total_cost_usd: float | None
    avg_cost_per_run: float | None
    avg_cost_per_problem: float | None





    def to_dict(self) -> dict[str, Any]:
        user_id = str(self.user_id)

        user_name = self.user_name

        total_runs = self.total_runs

        avg_score: float | None
        avg_score = self.avg_score

        total_cost_usd: float | None
        total_cost_usd = self.total_cost_usd

        avg_cost_per_run: float | None
        avg_cost_per_run = self.avg_cost_per_run

        avg_cost_per_problem: float | None
        avg_cost_per_problem = self.avg_cost_per_problem


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "userId": user_id,
            "userName": user_name,
            "totalRuns": total_runs,
            "avgScore": avg_score,
            "totalCostUsd": total_cost_usd,
            "avgCostPerRun": avg_cost_per_run,
            "avgCostPerProblem": avg_cost_per_problem,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        user_id = UUID(d.pop("userId"))




        user_name = d.pop("userName")

        total_runs = d.pop("totalRuns")

        def _parse_avg_score(data: object) -> float | None:
            if data is None:
                return data
            return cast(float | None, data)

        avg_score = _parse_avg_score(d.pop("avgScore"))


        def _parse_total_cost_usd(data: object) -> float | None:
            if data is None:
                return data
            return cast(float | None, data)

        total_cost_usd = _parse_total_cost_usd(d.pop("totalCostUsd"))


        def _parse_avg_cost_per_run(data: object) -> float | None:
            if data is None:
                return data
            return cast(float | None, data)

        avg_cost_per_run = _parse_avg_cost_per_run(d.pop("avgCostPerRun"))


        def _parse_avg_cost_per_problem(data: object) -> float | None:
            if data is None:
                return data
            return cast(float | None, data)

        avg_cost_per_problem = _parse_avg_cost_per_problem(d.pop("avgCostPerProblem"))


        user_efficiency_response_dto_rows_item = cls(
            user_id=user_id,
            user_name=user_name,
            total_runs=total_runs,
            avg_score=avg_score,
            total_cost_usd=total_cost_usd,
            avg_cost_per_run=avg_cost_per_run,
            avg_cost_per_problem=avg_cost_per_problem,
        )

        return user_efficiency_response_dto_rows_item

