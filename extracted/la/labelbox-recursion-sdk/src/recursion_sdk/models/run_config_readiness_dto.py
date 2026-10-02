from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.run_config_readiness_dto_solver_menu_issue_type_0 import RunConfigReadinessDtoSolverMenuIssueType0
from typing import cast






T = TypeVar("T", bound="RunConfigReadinessDto")



@_attrs_define
class RunConfigReadinessDto:
    """ Readiness of an environment's solver run-config menu for public execution. Existing seeded menus count as
    configured.

        Example:
            {'solverMenuReady': True, 'solverMenuIssue': None}

        Attributes:
            solver_menu_ready (bool): Whether the environment solver menu has at least one reachable, locked run-config
                version that can authorize public execution.
            solver_menu_issue (None | RunConfigReadinessDtoSolverMenuIssueType0): Actionable reason the solver menu is not
                ready, or null when solverMenuReady is true.
     """

    solver_menu_ready: bool
    solver_menu_issue: None | RunConfigReadinessDtoSolverMenuIssueType0





    def to_dict(self) -> dict[str, Any]:
        solver_menu_ready = self.solver_menu_ready

        solver_menu_issue: None | str
        if isinstance(self.solver_menu_issue, RunConfigReadinessDtoSolverMenuIssueType0):
            solver_menu_issue = self.solver_menu_issue.value
        else:
            solver_menu_issue = self.solver_menu_issue


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "solverMenuReady": solver_menu_ready,
            "solverMenuIssue": solver_menu_issue,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        solver_menu_ready = d.pop("solverMenuReady")

        def _parse_solver_menu_issue(data: object) -> None | RunConfigReadinessDtoSolverMenuIssueType0:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                solver_menu_issue_type_0 = RunConfigReadinessDtoSolverMenuIssueType0(data)



                return solver_menu_issue_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | RunConfigReadinessDtoSolverMenuIssueType0, data)

        solver_menu_issue = _parse_solver_menu_issue(d.pop("solverMenuIssue"))


        run_config_readiness_dto = cls(
            solver_menu_ready=solver_menu_ready,
            solver_menu_issue=solver_menu_issue,
        )

        return run_config_readiness_dto

