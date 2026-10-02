from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast






T = TypeVar("T", bound="ProblemCostStatusDto")



@_attrs_define
class ProblemCostStatusDto:
    """ Per-problem cost-limit status: how close each applicable cap is to being exhausted, and whether any cap has been
    exceeded.

        Example:
            {'problemLimitPercentUsed': 30, 'problemLimitExceeded': False, 'environmentLimitPercentUsed': 30,
                'environmentLimitExceeded': False, 'specificProblemLimitPercentUsed': None, 'specificProblemLimitExceeded':
                False, 'hasSpecificProblemLimit': False}

        Attributes:
            problem_limit_percent_used (float | None): Percent of the most restrictive per-problem cap currently used, or
                null when no per-problem cap is in effect. Always in [0, 100].
            problem_limit_exceeded (bool): True when the most restrictive per-problem cap that applies to this problem has
                been reached.
            environment_limit_percent_used (float | None): Percent of the environment-wide cap currently used, or null when
                no environment cap is configured.
            environment_limit_exceeded (bool): True when the environment-wide cap has been reached.
            specific_problem_limit_percent_used (float | None): Percent of the problem-specific cap currently used, or null
                when no problem-specific cap is configured for this problem.
            specific_problem_limit_exceeded (bool): True when the problem-specific cap for this problem has been reached.
            has_specific_problem_limit (bool): True when a cost limit is configured specifically for this problem (vs. only
                an environment-wide cap).
     """

    problem_limit_percent_used: float | None
    problem_limit_exceeded: bool
    environment_limit_percent_used: float | None
    environment_limit_exceeded: bool
    specific_problem_limit_percent_used: float | None
    specific_problem_limit_exceeded: bool
    has_specific_problem_limit: bool





    def to_dict(self) -> dict[str, Any]:
        problem_limit_percent_used: float | None
        problem_limit_percent_used = self.problem_limit_percent_used

        problem_limit_exceeded = self.problem_limit_exceeded

        environment_limit_percent_used: float | None
        environment_limit_percent_used = self.environment_limit_percent_used

        environment_limit_exceeded = self.environment_limit_exceeded

        specific_problem_limit_percent_used: float | None
        specific_problem_limit_percent_used = self.specific_problem_limit_percent_used

        specific_problem_limit_exceeded = self.specific_problem_limit_exceeded

        has_specific_problem_limit = self.has_specific_problem_limit


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "problemLimitPercentUsed": problem_limit_percent_used,
            "problemLimitExceeded": problem_limit_exceeded,
            "environmentLimitPercentUsed": environment_limit_percent_used,
            "environmentLimitExceeded": environment_limit_exceeded,
            "specificProblemLimitPercentUsed": specific_problem_limit_percent_used,
            "specificProblemLimitExceeded": specific_problem_limit_exceeded,
            "hasSpecificProblemLimit": has_specific_problem_limit,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        def _parse_problem_limit_percent_used(data: object) -> float | None:
            if data is None:
                return data
            return cast(float | None, data)

        problem_limit_percent_used = _parse_problem_limit_percent_used(d.pop("problemLimitPercentUsed"))


        problem_limit_exceeded = d.pop("problemLimitExceeded")

        def _parse_environment_limit_percent_used(data: object) -> float | None:
            if data is None:
                return data
            return cast(float | None, data)

        environment_limit_percent_used = _parse_environment_limit_percent_used(d.pop("environmentLimitPercentUsed"))


        environment_limit_exceeded = d.pop("environmentLimitExceeded")

        def _parse_specific_problem_limit_percent_used(data: object) -> float | None:
            if data is None:
                return data
            return cast(float | None, data)

        specific_problem_limit_percent_used = _parse_specific_problem_limit_percent_used(d.pop("specificProblemLimitPercentUsed"))


        specific_problem_limit_exceeded = d.pop("specificProblemLimitExceeded")

        has_specific_problem_limit = d.pop("hasSpecificProblemLimit")

        problem_cost_status_dto = cls(
            problem_limit_percent_used=problem_limit_percent_used,
            problem_limit_exceeded=problem_limit_exceeded,
            environment_limit_percent_used=environment_limit_percent_used,
            environment_limit_exceeded=environment_limit_exceeded,
            specific_problem_limit_percent_used=specific_problem_limit_percent_used,
            specific_problem_limit_exceeded=specific_problem_limit_exceeded,
            has_specific_problem_limit=has_specific_problem_limit,
        )

        return problem_cost_status_dto

