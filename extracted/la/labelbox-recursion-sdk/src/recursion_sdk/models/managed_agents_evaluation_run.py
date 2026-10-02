from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.managed_agents_evaluation_run_execution_state import ManagedAgentsEvaluationRunExecutionState
from ..models.managed_agents_session_status import ManagedAgentsSessionStatus
from ..types import UNSET, Unset
from typing import cast
from uuid import UUID
import datetime






T = TypeVar("T", bound="ManagedAgentsEvaluationRun")



@_attrs_define
class ManagedAgentsEvaluationRun:
    """ One evaluation-run summary with frozen target count and authoritative verdict totals.

        Example:
            {'created_at': '2026-02-18T09:30:00Z', 'evaluator_agent_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d',
                'evaluator_agent_version_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'execution_state': 'provisioning',
                'fail_count': 1, 'not_applicable_count': 1, 'pass_count': 1, 'run_session_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'status': 'active', 'targets_total': 1, 'updated_at':
                '2026-02-18T09:30:00Z', 'verdicts_total': 1}

        Attributes:
            created_at (datetime.datetime): UTC timestamp when the evaluation run was created.
            evaluator_agent_id (UUID): Evaluation agent selected for the run.
            evaluator_agent_version_id (UUID): Immutable evaluator version and rubric frozen by the run.
            fail_count (int): Number of immutable overall fail verdicts in the run.
            not_applicable_count (int): Number of immutable not-applicable verdicts in the run.
            pass_count (int): Number of immutable overall pass verdicts in the run.
            run_session_id (UUID): Platform-internal root session coordinating this evaluation run.
            status (ManagedAgentsSessionStatus): Coarse session state shared by Managed Agents and imported RL rollouts.
                Example: active.
            targets_total (int): Number of target snapshots frozen into the run plan.
            updated_at (datetime.datetime): UTC timestamp of the latest run-session state change.
            verdicts_total (int): Total authoritative verdicts, equal to pass plus fail plus not applicable.
            execution_state (ManagedAgentsEvaluationRunExecutionState | Unset): Current agent-loop state when available on
                the run session.
     """

    created_at: datetime.datetime
    evaluator_agent_id: UUID
    evaluator_agent_version_id: UUID
    fail_count: int
    not_applicable_count: int
    pass_count: int
    run_session_id: UUID
    status: ManagedAgentsSessionStatus
    targets_total: int
    updated_at: datetime.datetime
    verdicts_total: int
    execution_state: ManagedAgentsEvaluationRunExecutionState | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        created_at = self.created_at.isoformat()

        evaluator_agent_id = str(self.evaluator_agent_id)

        evaluator_agent_version_id = str(self.evaluator_agent_version_id)

        fail_count = self.fail_count

        not_applicable_count = self.not_applicable_count

        pass_count = self.pass_count

        run_session_id = str(self.run_session_id)

        status = self.status.value

        targets_total = self.targets_total

        updated_at = self.updated_at.isoformat()

        verdicts_total = self.verdicts_total

        execution_state: str | Unset = UNSET
        if not isinstance(self.execution_state, Unset):
            execution_state = self.execution_state.value



        field_dict: dict[str, Any] = {}

        field_dict.update({
            "created_at": created_at,
            "evaluator_agent_id": evaluator_agent_id,
            "evaluator_agent_version_id": evaluator_agent_version_id,
            "fail_count": fail_count,
            "not_applicable_count": not_applicable_count,
            "pass_count": pass_count,
            "run_session_id": run_session_id,
            "status": status,
            "targets_total": targets_total,
            "updated_at": updated_at,
            "verdicts_total": verdicts_total,
        })
        if execution_state is not UNSET:
            field_dict["execution_state"] = execution_state

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        created_at = datetime.datetime.fromisoformat(d.pop("created_at"))




        evaluator_agent_id = UUID(d.pop("evaluator_agent_id"))




        evaluator_agent_version_id = UUID(d.pop("evaluator_agent_version_id"))




        fail_count = d.pop("fail_count")

        not_applicable_count = d.pop("not_applicable_count")

        pass_count = d.pop("pass_count")

        run_session_id = UUID(d.pop("run_session_id"))




        status = ManagedAgentsSessionStatus(d.pop("status"))




        targets_total = d.pop("targets_total")

        updated_at = datetime.datetime.fromisoformat(d.pop("updated_at"))




        verdicts_total = d.pop("verdicts_total")

        _execution_state = d.pop("execution_state", UNSET)
        execution_state: ManagedAgentsEvaluationRunExecutionState | Unset
        if isinstance(_execution_state,  Unset):
            execution_state = UNSET
        else:
            execution_state = ManagedAgentsEvaluationRunExecutionState(_execution_state)




        managed_agents_evaluation_run = cls(
            created_at=created_at,
            evaluator_agent_id=evaluator_agent_id,
            evaluator_agent_version_id=evaluator_agent_version_id,
            fail_count=fail_count,
            not_applicable_count=not_applicable_count,
            pass_count=pass_count,
            run_session_id=run_session_id,
            status=status,
            targets_total=targets_total,
            updated_at=updated_at,
            verdicts_total=verdicts_total,
            execution_state=execution_state,
        )

        return managed_agents_evaluation_run

