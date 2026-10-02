from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="AdminStatsDtoCounts")



@_attrs_define
class AdminStatsDtoCounts:
    """ Top-line entity counts across the platform.

        Attributes:
            organizations (float): Total number of organizations on the platform.
            environments (float): Total number of environments across all organizations.
            problems (float): Total number of problems across all environments.
            problem_runs (float): Total number of problem runs ever executed.
     """

    organizations: float
    environments: float
    problems: float
    problem_runs: float





    def to_dict(self) -> dict[str, Any]:
        organizations = self.organizations

        environments = self.environments

        problems = self.problems

        problem_runs = self.problem_runs


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "organizations": organizations,
            "environments": environments,
            "problems": problems,
            "problemRuns": problem_runs,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        organizations = d.pop("organizations")

        environments = d.pop("environments")

        problems = d.pop("problems")

        problem_runs = d.pop("problemRuns")

        admin_stats_dto_counts = cls(
            organizations=organizations,
            environments=environments,
            problems=problems,
            problem_runs=problem_runs,
        )

        return admin_stats_dto_counts

