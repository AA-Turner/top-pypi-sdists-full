from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.managed_agents_outcome_evaluation_result import ManagedAgentsOutcomeEvaluationResult
from ..types import UNSET, Unset
from typing import cast
import datetime

if TYPE_CHECKING:
  from ..models.managed_agents_outcome_criterion import ManagedAgentsOutcomeCriterion





T = TypeVar("T", bound="ManagedAgentsOutcomeEvaluation")



@_attrs_define
class ManagedAgentsOutcomeEvaluation:
    """ One grader pass over the work, with its verdict, its per-criterion scoring, and what it cost. A caller sees these in
    an outcome's evaluations list, one per revision round.

        Example:
            {'agent_version_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'cache_read_tokens': 1, 'cache_write_tokens': 1,
                'cost_micros': 1, 'criteria': [{'criterion_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'criterion_text':
                'example', 'evidence_event_ids': ['example'], 'rationale': 'example', 'section': 'example', 'verdict':
                'example', 'weight': 1.5}], 'end_event_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'ended_at':
                '2026-02-18T09:30:00Z', 'explanation': 'example', 'grader_model_ref_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d',
                'grader_thread_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'input_tokens': 1, 'iteration': 1, 'outcome_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'output_tokens': 1, 'result': 'satisfied', 'start_event_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'started_at': '2026-02-18T09:30:00Z'}

        Attributes:
            iteration (int): 0-indexed pass number: 0 is the first evaluation, 1 the re-evaluation after the first revision.
            outcome_id (str): Outcome this evaluation belongs to (UUID).
            result (ManagedAgentsOutcomeEvaluationResult): Verdict of this pass. needs_revision is the only non-terminal
                value and sends the agent back for another turn; the rest end the outcome.
            agent_version_id (str | Unset): Agent version whose work this pass judged (UUID), denormalized onto the criteria
                so cross-session criterion history is served by an index.
            cache_read_tokens (int | Unset): Prompt tokens served from the provider's cache for this unit of work.
            cache_write_tokens (int | Unset): Prompt tokens written to the provider's cache for this unit of work.
            cost_micros (int | Unset): Accrued cost in micro-USD (1,000,000 = 1 USD). Integer to avoid float rounding across
                many small charges.
            criteria (list[ManagedAgentsOutcomeCriterion] | Unset): Per-criterion verdicts this pass produced, in rubric
                order. Empty when the grader returned only an overall result.
            end_event_id (str | Unset): Event on the graded session's own transcript that recorded this pass's verdict.
                Locates where the pass landed.
            ended_at (datetime.datetime | Unset): RFC 3339 timestamp of when this grader pass finished. Absent while the
                pass is still in flight.
            explanation (str | Unset): Grader's message to the agent. For needs_revision this is the per-criterion gap list
                the next turn has to close.
            grader_model_ref_id (str | Unset): Model reference the grader actually ran on for this pass (UUID).
            grader_thread_id (str | Unset): Thread the grader ran in (UUID), so its own reasoning can be read back
                separately from the agent's transcript.
            input_tokens (int | Unset): Prompt tokens billed for this unit of work.
            output_tokens (int | Unset): Completion tokens billed for this unit of work.
            start_event_id (str | Unset): First event of the grader thread for this pass, which is the packet the harness
                handed it. Locates where the pass began.
            started_at (datetime.datetime | Unset): RFC 3339 timestamp of when this grader pass began.
     """

    iteration: int
    outcome_id: str
    result: ManagedAgentsOutcomeEvaluationResult
    agent_version_id: str | Unset = UNSET
    cache_read_tokens: int | Unset = UNSET
    cache_write_tokens: int | Unset = UNSET
    cost_micros: int | Unset = UNSET
    criteria: list[ManagedAgentsOutcomeCriterion] | Unset = UNSET
    end_event_id: str | Unset = UNSET
    ended_at: datetime.datetime | Unset = UNSET
    explanation: str | Unset = UNSET
    grader_model_ref_id: str | Unset = UNSET
    grader_thread_id: str | Unset = UNSET
    input_tokens: int | Unset = UNSET
    output_tokens: int | Unset = UNSET
    start_event_id: str | Unset = UNSET
    started_at: datetime.datetime | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.managed_agents_outcome_criterion import ManagedAgentsOutcomeCriterion # noqa: PLC0415
        iteration = self.iteration

        outcome_id = self.outcome_id

        result = self.result.value

        agent_version_id = self.agent_version_id

        cache_read_tokens = self.cache_read_tokens

        cache_write_tokens = self.cache_write_tokens

        cost_micros = self.cost_micros

        criteria: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.criteria, Unset):
            criteria = []
            for criteria_item_data in self.criteria:
                criteria_item = criteria_item_data.to_dict()
                criteria.append(criteria_item)



        end_event_id = self.end_event_id

        ended_at: str | Unset = UNSET
        if not isinstance(self.ended_at, Unset):
            ended_at = self.ended_at.isoformat()

        explanation = self.explanation

        grader_model_ref_id = self.grader_model_ref_id

        grader_thread_id = self.grader_thread_id

        input_tokens = self.input_tokens

        output_tokens = self.output_tokens

        start_event_id = self.start_event_id

        started_at: str | Unset = UNSET
        if not isinstance(self.started_at, Unset):
            started_at = self.started_at.isoformat()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "iteration": iteration,
            "outcome_id": outcome_id,
            "result": result,
        })
        if agent_version_id is not UNSET:
            field_dict["agent_version_id"] = agent_version_id
        if cache_read_tokens is not UNSET:
            field_dict["cache_read_tokens"] = cache_read_tokens
        if cache_write_tokens is not UNSET:
            field_dict["cache_write_tokens"] = cache_write_tokens
        if cost_micros is not UNSET:
            field_dict["cost_micros"] = cost_micros
        if criteria is not UNSET:
            field_dict["criteria"] = criteria
        if end_event_id is not UNSET:
            field_dict["end_event_id"] = end_event_id
        if ended_at is not UNSET:
            field_dict["ended_at"] = ended_at
        if explanation is not UNSET:
            field_dict["explanation"] = explanation
        if grader_model_ref_id is not UNSET:
            field_dict["grader_model_ref_id"] = grader_model_ref_id
        if grader_thread_id is not UNSET:
            field_dict["grader_thread_id"] = grader_thread_id
        if input_tokens is not UNSET:
            field_dict["input_tokens"] = input_tokens
        if output_tokens is not UNSET:
            field_dict["output_tokens"] = output_tokens
        if start_event_id is not UNSET:
            field_dict["start_event_id"] = start_event_id
        if started_at is not UNSET:
            field_dict["started_at"] = started_at

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.managed_agents_outcome_criterion import ManagedAgentsOutcomeCriterion # noqa: PLC0415
        d = dict(src_dict)
        iteration = d.pop("iteration")

        outcome_id = d.pop("outcome_id")

        result = ManagedAgentsOutcomeEvaluationResult(d.pop("result"))




        agent_version_id = d.pop("agent_version_id", UNSET)

        cache_read_tokens = d.pop("cache_read_tokens", UNSET)

        cache_write_tokens = d.pop("cache_write_tokens", UNSET)

        cost_micros = d.pop("cost_micros", UNSET)

        _criteria = d.pop("criteria", UNSET)
        criteria: list[ManagedAgentsOutcomeCriterion] | Unset = UNSET
        if _criteria is not UNSET:
            criteria = []
            for criteria_item_data in _criteria:
                criteria_item = ManagedAgentsOutcomeCriterion.from_dict(criteria_item_data)



                criteria.append(criteria_item)


        end_event_id = d.pop("end_event_id", UNSET)

        _ended_at = d.pop("ended_at", UNSET)
        ended_at: datetime.datetime | Unset
        if isinstance(_ended_at,  Unset):
            ended_at = UNSET
        else:
            ended_at = datetime.datetime.fromisoformat(_ended_at)




        explanation = d.pop("explanation", UNSET)

        grader_model_ref_id = d.pop("grader_model_ref_id", UNSET)

        grader_thread_id = d.pop("grader_thread_id", UNSET)

        input_tokens = d.pop("input_tokens", UNSET)

        output_tokens = d.pop("output_tokens", UNSET)

        start_event_id = d.pop("start_event_id", UNSET)

        _started_at = d.pop("started_at", UNSET)
        started_at: datetime.datetime | Unset
        if isinstance(_started_at,  Unset):
            started_at = UNSET
        else:
            started_at = datetime.datetime.fromisoformat(_started_at)




        managed_agents_outcome_evaluation = cls(
            iteration=iteration,
            outcome_id=outcome_id,
            result=result,
            agent_version_id=agent_version_id,
            cache_read_tokens=cache_read_tokens,
            cache_write_tokens=cache_write_tokens,
            cost_micros=cost_micros,
            criteria=criteria,
            end_event_id=end_event_id,
            ended_at=ended_at,
            explanation=explanation,
            grader_model_ref_id=grader_model_ref_id,
            grader_thread_id=grader_thread_id,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            start_event_id=start_event_id,
            started_at=started_at,
        )


        managed_agents_outcome_evaluation.additional_properties = d
        return managed_agents_outcome_evaluation

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
