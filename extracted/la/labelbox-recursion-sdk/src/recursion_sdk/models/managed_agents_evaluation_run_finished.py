from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.managed_agents_evaluation_run_finished_failure_code import ManagedAgentsEvaluationRunFinishedFailureCode
from ..models.managed_agents_evaluation_run_finished_terminal_status import ManagedAgentsEvaluationRunFinishedTerminalStatus
from ..types import UNSET, Unset






T = TypeVar("T", bound="ManagedAgentsEvaluationRunFinished")



@_attrs_define
class ManagedAgentsEvaluationRunFinished:
    """ Terminal audit payload summarizing planned targets, completed verdict audits, skips, budget stops, and any systemic
    failure.

        Example:
            {'failure_code': 'plan_failed', 'failure_message': 'example', 'targets_budget_reached': 1, 'targets_skipped': 1,
                'targets_total': 1, 'terminal_status': 'completed', 'verdicts_recorded': 1}

        Attributes:
            targets_budget_reached (int): Number of targets stopped or not admitted after the cost cap was reached.
            targets_skipped (int): Number of targets whose processing ended without a completed verdict audit.
            targets_total (int): Number of target snapshots frozen in the plan.
            terminal_status (ManagedAgentsEvaluationRunFinishedTerminalStatus): Final lifecycle state of the evaluation run.
            verdicts_recorded (int): Number of completed verdict audit events recorded for this run.
            failure_code (ManagedAgentsEvaluationRunFinishedFailureCode | Unset): Stable systemic failure classification for
                a failed run.
            failure_message (str | Unset): Sanitized explanation of the systemic run failure.
     """

    targets_budget_reached: int
    targets_skipped: int
    targets_total: int
    terminal_status: ManagedAgentsEvaluationRunFinishedTerminalStatus
    verdicts_recorded: int
    failure_code: ManagedAgentsEvaluationRunFinishedFailureCode | Unset = UNSET
    failure_message: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        targets_budget_reached = self.targets_budget_reached

        targets_skipped = self.targets_skipped

        targets_total = self.targets_total

        terminal_status = self.terminal_status.value

        verdicts_recorded = self.verdicts_recorded

        failure_code: str | Unset = UNSET
        if not isinstance(self.failure_code, Unset):
            failure_code = self.failure_code.value


        failure_message = self.failure_message


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "targets_budget_reached": targets_budget_reached,
            "targets_skipped": targets_skipped,
            "targets_total": targets_total,
            "terminal_status": terminal_status,
            "verdicts_recorded": verdicts_recorded,
        })
        if failure_code is not UNSET:
            field_dict["failure_code"] = failure_code
        if failure_message is not UNSET:
            field_dict["failure_message"] = failure_message

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        targets_budget_reached = d.pop("targets_budget_reached")

        targets_skipped = d.pop("targets_skipped")

        targets_total = d.pop("targets_total")

        terminal_status = ManagedAgentsEvaluationRunFinishedTerminalStatus(d.pop("terminal_status"))




        verdicts_recorded = d.pop("verdicts_recorded")

        _failure_code = d.pop("failure_code", UNSET)
        failure_code: ManagedAgentsEvaluationRunFinishedFailureCode | Unset
        if isinstance(_failure_code,  Unset):
            failure_code = UNSET
        else:
            failure_code = ManagedAgentsEvaluationRunFinishedFailureCode(_failure_code)




        failure_message = d.pop("failure_message", UNSET)

        managed_agents_evaluation_run_finished = cls(
            targets_budget_reached=targets_budget_reached,
            targets_skipped=targets_skipped,
            targets_total=targets_total,
            terminal_status=terminal_status,
            verdicts_recorded=verdicts_recorded,
            failure_code=failure_code,
            failure_message=failure_message,
        )

        return managed_agents_evaluation_run_finished

