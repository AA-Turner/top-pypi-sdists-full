from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.managed_agents_evaluation_run_finished_request_failure_code import ManagedAgentsEvaluationRunFinishedRequestFailureCode
from ..models.managed_agents_evaluation_run_finished_request_terminal_status import ManagedAgentsEvaluationRunFinishedRequestTerminalStatus
from ..types import UNSET, Unset






T = TypeVar("T", bound="ManagedAgentsEvaluationRunFinishedRequest")



@_attrs_define
class ManagedAgentsEvaluationRunFinishedRequest:
    """ Terminal audit payload summarizing planned targets, completed verdict audits, skips, budget stops, and any systemic
    failure.

        Example:
            {'failure_code': 'plan_failed', 'failure_message': 'example', 'targets_budget_reached': 1, 'targets_skipped': 1,
                'targets_total': 1, 'terminal_status': 'completed', 'verdicts_recorded': 1}

        Attributes:
            failure_code (ManagedAgentsEvaluationRunFinishedRequestFailureCode | Unset): Stable systemic failure
                classification for a failed run.
            failure_message (str | Unset): Sanitized explanation of the systemic run failure.
            targets_budget_reached (int | Unset): Number of targets stopped or not admitted after the cost cap was reached.
            targets_skipped (int | Unset): Number of targets whose processing ended without a completed verdict audit.
            targets_total (int | Unset): Number of target snapshots frozen in the plan.
            terminal_status (ManagedAgentsEvaluationRunFinishedRequestTerminalStatus | Unset): Final lifecycle state of the
                evaluation run.
            verdicts_recorded (int | Unset): Number of completed verdict audit events recorded for this run.
     """

    failure_code: ManagedAgentsEvaluationRunFinishedRequestFailureCode | Unset = UNSET
    failure_message: str | Unset = UNSET
    targets_budget_reached: int | Unset = UNSET
    targets_skipped: int | Unset = UNSET
    targets_total: int | Unset = UNSET
    terminal_status: ManagedAgentsEvaluationRunFinishedRequestTerminalStatus | Unset = UNSET
    verdicts_recorded: int | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        failure_code: str | Unset = UNSET
        if not isinstance(self.failure_code, Unset):
            failure_code = self.failure_code.value


        failure_message = self.failure_message

        targets_budget_reached = self.targets_budget_reached

        targets_skipped = self.targets_skipped

        targets_total = self.targets_total

        terminal_status: str | Unset = UNSET
        if not isinstance(self.terminal_status, Unset):
            terminal_status = self.terminal_status.value


        verdicts_recorded = self.verdicts_recorded


        field_dict: dict[str, Any] = {}

        field_dict.update({
        })
        if failure_code is not UNSET:
            field_dict["failure_code"] = failure_code
        if failure_message is not UNSET:
            field_dict["failure_message"] = failure_message
        if targets_budget_reached is not UNSET:
            field_dict["targets_budget_reached"] = targets_budget_reached
        if targets_skipped is not UNSET:
            field_dict["targets_skipped"] = targets_skipped
        if targets_total is not UNSET:
            field_dict["targets_total"] = targets_total
        if terminal_status is not UNSET:
            field_dict["terminal_status"] = terminal_status
        if verdicts_recorded is not UNSET:
            field_dict["verdicts_recorded"] = verdicts_recorded

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _failure_code = d.pop("failure_code", UNSET)
        failure_code: ManagedAgentsEvaluationRunFinishedRequestFailureCode | Unset
        if isinstance(_failure_code,  Unset):
            failure_code = UNSET
        else:
            failure_code = ManagedAgentsEvaluationRunFinishedRequestFailureCode(_failure_code)




        failure_message = d.pop("failure_message", UNSET)

        targets_budget_reached = d.pop("targets_budget_reached", UNSET)

        targets_skipped = d.pop("targets_skipped", UNSET)

        targets_total = d.pop("targets_total", UNSET)

        _terminal_status = d.pop("terminal_status", UNSET)
        terminal_status: ManagedAgentsEvaluationRunFinishedRequestTerminalStatus | Unset
        if isinstance(_terminal_status,  Unset):
            terminal_status = UNSET
        else:
            terminal_status = ManagedAgentsEvaluationRunFinishedRequestTerminalStatus(_terminal_status)




        verdicts_recorded = d.pop("verdicts_recorded", UNSET)

        managed_agents_evaluation_run_finished_request = cls(
            failure_code=failure_code,
            failure_message=failure_message,
            targets_budget_reached=targets_budget_reached,
            targets_skipped=targets_skipped,
            targets_total=targets_total,
            terminal_status=terminal_status,
            verdicts_recorded=verdicts_recorded,
        )

        return managed_agents_evaluation_run_finished_request

