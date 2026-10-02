from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.managed_agents_outcome import ManagedAgentsOutcome





T = TypeVar("T", bound="ManagedAgentsOutcomeListResponse")



@_attrs_define
class ManagedAgentsOutcomeListResponse:
    """ Response body of GET /v1/sessions/{session_id}/outcomes. An outcome is the structured verdict a grader or the agent
    itself writes for a session; a session may accumulate more than one, so this is a list rather than a single object.

        Example:
            {'outcomes': [{'agent_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'created_at': '2026-02-18T09:30:00Z',
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
                '2026-02-18T09:30:00Z'}]}

        Attributes:
            outcomes (list[ManagedAgentsOutcome] | None): Outcomes recorded against the session named in the path. Null
                rather than an empty array when none has been recorded, which is the normal state for a session that is still
                running.
     """

    outcomes: list[ManagedAgentsOutcome] | None
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.managed_agents_outcome import ManagedAgentsOutcome # noqa: PLC0415
        outcomes: list[dict[str, Any]] | None
        if isinstance(self.outcomes, list):
            outcomes = []
            for outcomes_type_0_item_data in self.outcomes:
                outcomes_type_0_item = outcomes_type_0_item_data.to_dict()
                outcomes.append(outcomes_type_0_item)


        else:
            outcomes = self.outcomes


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "outcomes": outcomes,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.managed_agents_outcome import ManagedAgentsOutcome # noqa: PLC0415
        d = dict(src_dict)
        def _parse_outcomes(data: object) -> list[ManagedAgentsOutcome] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                outcomes_type_0 = []
                _outcomes_type_0 = data
                for outcomes_type_0_item_data in (_outcomes_type_0):
                    outcomes_type_0_item = ManagedAgentsOutcome.from_dict(outcomes_type_0_item_data)



                    outcomes_type_0.append(outcomes_type_0_item)

                return outcomes_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[ManagedAgentsOutcome] | None, data)

        outcomes = _parse_outcomes(d.pop("outcomes"))


        managed_agents_outcome_list_response = cls(
            outcomes=outcomes,
        )


        managed_agents_outcome_list_response.additional_properties = d
        return managed_agents_outcome_list_response

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
