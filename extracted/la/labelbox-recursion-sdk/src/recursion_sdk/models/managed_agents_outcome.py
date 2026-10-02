from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.managed_agents_outcome_status import ManagedAgentsOutcomeStatus
from ..models.managed_agents_outcome_terminal_result import ManagedAgentsOutcomeTerminalResult
from ..types import UNSET, Unset
from typing import cast
import datetime

if TYPE_CHECKING:
  from ..models.managed_agents_outcome_evaluation import ManagedAgentsOutcomeEvaluation





T = TypeVar("T", bound="ManagedAgentsOutcome")



@_attrs_define
class ManagedAgentsOutcome:
    """ A session's definition of done: the task to achieve plus a rubric a grader scores the work against, tracked through
    its own grading lifecycle. Defined when the session starts, and read back to see whether the work was accepted.

        Example:
            {'agent_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'created_at': '2026-02-18T09:30:00Z',
                'defined_by_event_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'description': 'example', 'ended_at':
                '2026-02-18T09:30:00Z', 'evaluations': [{'agent_version_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d',
                'cache_read_tokens': 1, 'cache_write_tokens': 1, 'cost_micros': 1, 'criteria': [{'criterion_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'criterion_text': 'example', 'evidence_event_ids': ['example'],
                'rationale': 'example', 'section': 'example', 'verdict': 'example', 'weight': 1.5}], 'end_event_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'ended_at': '2026-02-18T09:30:00Z', 'explanation': 'example',
                'grader_model_ref_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'grader_thread_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'input_tokens': 1, 'iteration': 1, 'outcome_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'output_tokens': 1, 'result': 'satisfied', 'start_event_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'started_at': '2026-02-18T09:30:00Z'}], 'grader_model_ref_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'max_iterations': 1, 'organization_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'outcome_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'rubric':
                'example', 'rubric_ref': 'example', 'rubric_sha256': 'example', 'session_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'status': 'pending', 'terminal_result': 'satisfied', 'updated_at':
                '2026-02-18T09:30:00Z'}

        Attributes:
            created_at (datetime.datetime): RFC 3339 timestamp of when this record was created. Server-assigned.
            description (str): Objective the agent works toward, in prose, and the statement of it quoted to the grader.
                Opens the session when the start request carries no message.
            max_iterations (int): Ceiling on grader passes before the outcome ends as max_iterations_reached. Zero means
                unbounded, which is the default: the loop runs until the grader is satisfied.
            organization_id (str): Organization that owns this record. Resolved from the API key; never accepted from the
                caller.
            outcome_id (str): Identifier for this outcome (UUID). Server-assigned.
            rubric (str): Markdown rubric the grader scores the work against. Write independently checkable criteria; vague
                criteria produce noisy revision loops.
            session_id (str): Session this outcome belongs to (UUID).
            status (ManagedAgentsOutcomeStatus): Where the outcome is in its grading lifecycle: pending (no grader has
                looked at it), running (the agent is working toward it), evaluating (a grader pass is in flight), or terminal
                (grading finished; read terminal_result).
            updated_at (datetime.datetime): RFC 3339 timestamp of the last change to this record. Server-assigned.
            agent_id (str | Unset): Agent this outcome belongs to (UUID), copied from the session that defined it.
            defined_by_event_id (str | Unset): Event in the session's log that defined this outcome (UUID).
            ended_at (datetime.datetime | Unset): RFC 3339 timestamp of when grading reached a terminal result. Absent while
                the outcome is still open.
            evaluations (list[ManagedAgentsOutcomeEvaluation] | Unset): Grader passes in order, newest last. Returned only
                by reads that ask for evaluations, and empty until a grader has run.
            grader_model_ref_id (str | Unset): Model reference the grader runs on (UUID), letting grading use a different
                model than the agent doing the work. Defaults to the session's model.
            rubric_ref (str | Unset): Where the rubric text came from when it was not sent inline: file:<file_id> for a
                rubric read from a file when the outcome was defined. rubric always carries the text; later changes to the file
                do not move the bar.
            rubric_sha256 (str | Unset): Lowercase SHA-256 digest of the uploaded file the rubric was read from, for
                matching it to the file. Not a digest of rubric: the recorded text is the file's minus a byte-order mark and
                with line endings normalized.
            terminal_result (ManagedAgentsOutcomeTerminalResult | Unset): Final verdict, set only once status is terminal:
                satisfied, max_iterations_reached, failed, or interrupted. Empty before then.
     """

    created_at: datetime.datetime
    description: str
    max_iterations: int
    organization_id: str
    outcome_id: str
    rubric: str
    session_id: str
    status: ManagedAgentsOutcomeStatus
    updated_at: datetime.datetime
    agent_id: str | Unset = UNSET
    defined_by_event_id: str | Unset = UNSET
    ended_at: datetime.datetime | Unset = UNSET
    evaluations: list[ManagedAgentsOutcomeEvaluation] | Unset = UNSET
    grader_model_ref_id: str | Unset = UNSET
    rubric_ref: str | Unset = UNSET
    rubric_sha256: str | Unset = UNSET
    terminal_result: ManagedAgentsOutcomeTerminalResult | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.managed_agents_outcome_evaluation import ManagedAgentsOutcomeEvaluation # noqa: PLC0415
        created_at = self.created_at.isoformat()

        description = self.description

        max_iterations = self.max_iterations

        organization_id = self.organization_id

        outcome_id = self.outcome_id

        rubric = self.rubric

        session_id = self.session_id

        status = self.status.value

        updated_at = self.updated_at.isoformat()

        agent_id = self.agent_id

        defined_by_event_id = self.defined_by_event_id

        ended_at: str | Unset = UNSET
        if not isinstance(self.ended_at, Unset):
            ended_at = self.ended_at.isoformat()

        evaluations: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.evaluations, Unset):
            evaluations = []
            for evaluations_item_data in self.evaluations:
                evaluations_item = evaluations_item_data.to_dict()
                evaluations.append(evaluations_item)



        grader_model_ref_id = self.grader_model_ref_id

        rubric_ref = self.rubric_ref

        rubric_sha256 = self.rubric_sha256

        terminal_result: str | Unset = UNSET
        if not isinstance(self.terminal_result, Unset):
            terminal_result = self.terminal_result.value



        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "created_at": created_at,
            "description": description,
            "max_iterations": max_iterations,
            "organization_id": organization_id,
            "outcome_id": outcome_id,
            "rubric": rubric,
            "session_id": session_id,
            "status": status,
            "updated_at": updated_at,
        })
        if agent_id is not UNSET:
            field_dict["agent_id"] = agent_id
        if defined_by_event_id is not UNSET:
            field_dict["defined_by_event_id"] = defined_by_event_id
        if ended_at is not UNSET:
            field_dict["ended_at"] = ended_at
        if evaluations is not UNSET:
            field_dict["evaluations"] = evaluations
        if grader_model_ref_id is not UNSET:
            field_dict["grader_model_ref_id"] = grader_model_ref_id
        if rubric_ref is not UNSET:
            field_dict["rubric_ref"] = rubric_ref
        if rubric_sha256 is not UNSET:
            field_dict["rubric_sha256"] = rubric_sha256
        if terminal_result is not UNSET:
            field_dict["terminal_result"] = terminal_result

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.managed_agents_outcome_evaluation import ManagedAgentsOutcomeEvaluation # noqa: PLC0415
        d = dict(src_dict)
        created_at = datetime.datetime.fromisoformat(d.pop("created_at"))




        description = d.pop("description")

        max_iterations = d.pop("max_iterations")

        organization_id = d.pop("organization_id")

        outcome_id = d.pop("outcome_id")

        rubric = d.pop("rubric")

        session_id = d.pop("session_id")

        status = ManagedAgentsOutcomeStatus(d.pop("status"))




        updated_at = datetime.datetime.fromisoformat(d.pop("updated_at"))




        agent_id = d.pop("agent_id", UNSET)

        defined_by_event_id = d.pop("defined_by_event_id", UNSET)

        _ended_at = d.pop("ended_at", UNSET)
        ended_at: datetime.datetime | Unset
        if isinstance(_ended_at,  Unset):
            ended_at = UNSET
        else:
            ended_at = datetime.datetime.fromisoformat(_ended_at)




        _evaluations = d.pop("evaluations", UNSET)
        evaluations: list[ManagedAgentsOutcomeEvaluation] | Unset = UNSET
        if _evaluations is not UNSET:
            evaluations = []
            for evaluations_item_data in _evaluations:
                evaluations_item = ManagedAgentsOutcomeEvaluation.from_dict(evaluations_item_data)



                evaluations.append(evaluations_item)


        grader_model_ref_id = d.pop("grader_model_ref_id", UNSET)

        rubric_ref = d.pop("rubric_ref", UNSET)

        rubric_sha256 = d.pop("rubric_sha256", UNSET)

        _terminal_result = d.pop("terminal_result", UNSET)
        terminal_result: ManagedAgentsOutcomeTerminalResult | Unset
        if isinstance(_terminal_result,  Unset):
            terminal_result = UNSET
        else:
            terminal_result = ManagedAgentsOutcomeTerminalResult(_terminal_result)




        managed_agents_outcome = cls(
            created_at=created_at,
            description=description,
            max_iterations=max_iterations,
            organization_id=organization_id,
            outcome_id=outcome_id,
            rubric=rubric,
            session_id=session_id,
            status=status,
            updated_at=updated_at,
            agent_id=agent_id,
            defined_by_event_id=defined_by_event_id,
            ended_at=ended_at,
            evaluations=evaluations,
            grader_model_ref_id=grader_model_ref_id,
            rubric_ref=rubric_ref,
            rubric_sha256=rubric_sha256,
            terminal_result=terminal_result,
        )


        managed_agents_outcome.additional_properties = d
        return managed_agents_outcome

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
