from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.managed_agents_automation_run_defaults_metadata import ManagedAgentsAutomationRunDefaultsMetadata
  from ..models.managed_agents_automation_run_defaults_payload import ManagedAgentsAutomationRunDefaultsPayload
  from ..models.managed_agents_evaluation_selector import ManagedAgentsEvaluationSelector
  from ..models.managed_agents_memory_store_attachment import ManagedAgentsMemoryStoreAttachment
  from ..models.managed_agents_new_event import ManagedAgentsNewEvent
  from ..models.managed_agents_new_outcome import ManagedAgentsNewOutcome
  from ..models.managed_agents_session_resource_ref import ManagedAgentsSessionResourceRef





T = TypeVar("T", bound="ManagedAgentsAutomationRunDefaults")



@_attrs_define
class ManagedAgentsAutomationRunDefaults:
    """ The session shape every run of an automation produces, copied onto each run rather than shared between them.

        Example:
            {'evaluation': {'limit': 1, 'session_ids': ['example'], 'statuses': ['active']}, 'initial_events': [{'actor':
                'human:api', 'agent_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'cache_read_tokens': 1, 'cache_write_tokens':
                1, 'causal_event_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'content': {'blocks': [{'byte_size': 1, 'content':
                [], 'context': 'example', 'data': 'example', 'encrypted_content': 'example', 'height': 1, 'id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'input': {'key': 'example'}, 'is_error': True, 'media_type': 'example',
                'name': 'example-name', 'omitted_bytes': 1, 'payload': 'example', 'provider': 'example', 'provider_payload':
                'example', 'redacted': True, 'semantic_hint': 'example', 'sha256': 'example', 'signature': 'example', 'source':
                {'file_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'type': 'file'}, 'summary': [], 'text': 'example', 'title':
                'example', 'tool_use_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'type': 'example', 'uri': 'example', 'url':
                'https://example.com', 'url_expires_at': '2026-02-18T09:30:00Z', 'width': 1}], 'evaluation_budget_reached':
                {'affected_target_session_ids': ['9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d'], 'max_tree_cost_usd': 'example'},
                'evaluation_plan_frozen': {'criteria': [{'criterion_key': 'example', 'criterion_text': 'example'}],
                'max_concurrent_threads': 1, 'max_tree_cost_usd': 'example', 'targets': [{'snapshot_event_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'target_session_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d'}]},
                'evaluation_run_finished': {'failure_code': 'plan_failed', 'failure_message': 'example',
                'targets_budget_reached': 1, 'targets_skipped': 1, 'targets_total': 1, 'terminal_status': 'completed',
                'verdicts_recorded': 1}, 'evaluation_target_skipped': {'child_session_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'reason': 'example', 'reason_code': 'child_create_failed',
                'snapshot_event_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'target_session_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d'}, 'evaluation_target_started': {'child_session_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'clone_state': 'ready', 'evaluation_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'sandbox_provider': 'example', 'snapshot_event_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'target_session_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d'},
                'evaluation_verdict_recorded': {'child_session_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'cost_completeness':
                'complete', 'cost_usd': 'example', 'evaluation_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d',
                'failed_criterion_keys': ['example'], 'result': 'pass', 'snapshot_event_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'target_session_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d'},
                'metadata': {'key': 'example'}, 'plan': [{'content': 'example', 'id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d',
                'status': 'example'}], 'stop_reason': 'example', 'tools': [{'description': 'example', 'input_schema': {'key':
                'example'}, 'name': 'example-name'}], 'usage': {'cache_read_tokens': 1, 'cache_write_tokens': 1, 'cost_usd':
                1.5, 'input_tokens': 1, 'output_tokens': 1}}, 'content_hydration_status': 'hydrated', 'content_payload_bytes':
                1, 'content_payload_ref': 'example', 'content_payload_sha256': 'example', 'content_ref': 'example',
                'cost_micros': 1, 'environment_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'event_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'event_status': 'example', 'event_type': 'example', 'finish_reason':
                'example', 'inference_config': {'max_tokens': 1, 'provider_params': {'key': 'example'}, 'reasoning_effort':
                'example', 'temperature': 1.5, 'top_p': 1.5}, 'input_tokens': 1, 'latency_ms': 1, 'model': {'base_url':
                'https://example.com', 'capabilities': {'key': 'example'}, 'context_window': 1, 'max_output_tokens': 1,
                'metadata': {'key': 'example'}, 'model': 'example', 'model_ref_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d',
                'model_version': 'example', 'provider': 'example', 'provider_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d',
                'provider_type': 'example', 'serving_backend': 'example'}, 'model_ref_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'organization_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d',
                'output_tokens': 1, 'parent_event_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'prompt_tokens': 1,
                'provider_model_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'provider_request_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'provider_type': 'example', 'role': 'user', 'sandbox_instance_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'schema_version': 1, 'thread_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'tool_name': 'example', 'tool_use_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'turn_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d'}], 'max_cost_usd':
                1.5, 'memory_stores': [{'access': 'read_only', 'instructions': 'example', 'memory_store_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d'}], 'metadata': {'key': 'example'}, 'outcome': {'description': 'example',
                'grader_model_ref_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'max_iterations': 1, 'rubric': 'example',
                'rubric_file_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d'}, 'payload': {'key': 'example'}, 'project_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'resources': [{'file_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d',
                'mount_path': 'example'}]}

        Attributes:
            evaluation (ManagedAgentsEvaluationSelector | Unset): A bounded evaluation target selector: explicit session
                ids, or statuses plus a newest-first limit. Example: {'limit': 1, 'session_ids': ['example'], 'statuses':
                ['active']}.
            initial_events (list[ManagedAgentsNewEvent] | Unset): Accepted and stored, but not yet applied to the sessions a
                run starts. Use initial_message until it is.
            max_cost_usd (float | Unset): Accepted and stored, but not yet applied to the sessions a run starts; a run is
                not capped by it today. Send null to clear.
            memory_stores (list[ManagedAgentsMemoryStoreAttachment] | Unset): Memory stores bound to every run.
            metadata (ManagedAgentsAutomationRunDefaultsMetadata | Unset): Caller-defined key/value metadata written onto
                every run's session and filterable when listing sessions.
            outcome (ManagedAgentsNewOutcome | Unset): A session's definition of done, graded against a rubric. The
                description is the objective the grader measures; a message sent alongside it is context the grader never sees.
                Example: {'description': 'example', 'grader_model_ref_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d',
                'max_iterations': 1, 'rubric': 'example', 'rubric_file_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d'}.
            payload (ManagedAgentsAutomationRunDefaultsPayload | Unset): Structured input rendered into the opening message
                for a scheduled run, which has no external event of its own.
            project_id (str | Unset): Labelbox project each run's work is attributed to. Overrides the agent version's
                default.
            resources (list[ManagedAgentsSessionResourceRef] | Unset): Files mounted into every run's sandbox, resolved and
                frozen when the run starts.
     """

    evaluation: ManagedAgentsEvaluationSelector | Unset = UNSET
    initial_events: list[ManagedAgentsNewEvent] | Unset = UNSET
    max_cost_usd: float | Unset = UNSET
    memory_stores: list[ManagedAgentsMemoryStoreAttachment] | Unset = UNSET
    metadata: ManagedAgentsAutomationRunDefaultsMetadata | Unset = UNSET
    outcome: ManagedAgentsNewOutcome | Unset = UNSET
    payload: ManagedAgentsAutomationRunDefaultsPayload | Unset = UNSET
    project_id: str | Unset = UNSET
    resources: list[ManagedAgentsSessionResourceRef] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.managed_agents_automation_run_defaults_metadata import ManagedAgentsAutomationRunDefaultsMetadata # noqa: PLC0415
        from ..models.managed_agents_automation_run_defaults_payload import ManagedAgentsAutomationRunDefaultsPayload # noqa: PLC0415
        from ..models.managed_agents_evaluation_selector import ManagedAgentsEvaluationSelector # noqa: PLC0415
        from ..models.managed_agents_memory_store_attachment import ManagedAgentsMemoryStoreAttachment # noqa: PLC0415
        from ..models.managed_agents_new_event import ManagedAgentsNewEvent # noqa: PLC0415
        from ..models.managed_agents_new_outcome import ManagedAgentsNewOutcome # noqa: PLC0415
        from ..models.managed_agents_session_resource_ref import ManagedAgentsSessionResourceRef # noqa: PLC0415
        evaluation: dict[str, Any] | Unset = UNSET
        if not isinstance(self.evaluation, Unset):
            evaluation = self.evaluation.to_dict()

        initial_events: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.initial_events, Unset):
            initial_events = []
            for initial_events_item_data in self.initial_events:
                initial_events_item = initial_events_item_data.to_dict()
                initial_events.append(initial_events_item)



        max_cost_usd = self.max_cost_usd

        memory_stores: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.memory_stores, Unset):
            memory_stores = []
            for memory_stores_item_data in self.memory_stores:
                memory_stores_item = memory_stores_item_data.to_dict()
                memory_stores.append(memory_stores_item)



        metadata: dict[str, Any] | Unset = UNSET
        if not isinstance(self.metadata, Unset):
            metadata = self.metadata.to_dict()

        outcome: dict[str, Any] | Unset = UNSET
        if not isinstance(self.outcome, Unset):
            outcome = self.outcome.to_dict()

        payload: dict[str, Any] | Unset = UNSET
        if not isinstance(self.payload, Unset):
            payload = self.payload.to_dict()

        project_id = self.project_id

        resources: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.resources, Unset):
            resources = []
            for resources_item_data in self.resources:
                resources_item = resources_item_data.to_dict()
                resources.append(resources_item)




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if evaluation is not UNSET:
            field_dict["evaluation"] = evaluation
        if initial_events is not UNSET:
            field_dict["initial_events"] = initial_events
        if max_cost_usd is not UNSET:
            field_dict["max_cost_usd"] = max_cost_usd
        if memory_stores is not UNSET:
            field_dict["memory_stores"] = memory_stores
        if metadata is not UNSET:
            field_dict["metadata"] = metadata
        if outcome is not UNSET:
            field_dict["outcome"] = outcome
        if payload is not UNSET:
            field_dict["payload"] = payload
        if project_id is not UNSET:
            field_dict["project_id"] = project_id
        if resources is not UNSET:
            field_dict["resources"] = resources

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.managed_agents_automation_run_defaults_metadata import ManagedAgentsAutomationRunDefaultsMetadata # noqa: PLC0415
        from ..models.managed_agents_automation_run_defaults_payload import ManagedAgentsAutomationRunDefaultsPayload # noqa: PLC0415
        from ..models.managed_agents_evaluation_selector import ManagedAgentsEvaluationSelector # noqa: PLC0415
        from ..models.managed_agents_memory_store_attachment import ManagedAgentsMemoryStoreAttachment # noqa: PLC0415
        from ..models.managed_agents_new_event import ManagedAgentsNewEvent # noqa: PLC0415
        from ..models.managed_agents_new_outcome import ManagedAgentsNewOutcome # noqa: PLC0415
        from ..models.managed_agents_session_resource_ref import ManagedAgentsSessionResourceRef # noqa: PLC0415
        d = dict(src_dict)
        _evaluation = d.pop("evaluation", UNSET)
        evaluation: ManagedAgentsEvaluationSelector | Unset
        if isinstance(_evaluation,  Unset):
            evaluation = UNSET
        else:
            evaluation = ManagedAgentsEvaluationSelector.from_dict(_evaluation)




        _initial_events = d.pop("initial_events", UNSET)
        initial_events: list[ManagedAgentsNewEvent] | Unset = UNSET
        if _initial_events is not UNSET:
            initial_events = []
            for initial_events_item_data in _initial_events:
                initial_events_item = ManagedAgentsNewEvent.from_dict(initial_events_item_data)



                initial_events.append(initial_events_item)


        max_cost_usd = d.pop("max_cost_usd", UNSET)

        _memory_stores = d.pop("memory_stores", UNSET)
        memory_stores: list[ManagedAgentsMemoryStoreAttachment] | Unset = UNSET
        if _memory_stores is not UNSET:
            memory_stores = []
            for memory_stores_item_data in _memory_stores:
                memory_stores_item = ManagedAgentsMemoryStoreAttachment.from_dict(memory_stores_item_data)



                memory_stores.append(memory_stores_item)


        _metadata = d.pop("metadata", UNSET)
        metadata: ManagedAgentsAutomationRunDefaultsMetadata | Unset
        if isinstance(_metadata,  Unset):
            metadata = UNSET
        else:
            metadata = ManagedAgentsAutomationRunDefaultsMetadata.from_dict(_metadata)




        _outcome = d.pop("outcome", UNSET)
        outcome: ManagedAgentsNewOutcome | Unset
        if isinstance(_outcome,  Unset):
            outcome = UNSET
        else:
            outcome = ManagedAgentsNewOutcome.from_dict(_outcome)




        _payload = d.pop("payload", UNSET)
        payload: ManagedAgentsAutomationRunDefaultsPayload | Unset
        if isinstance(_payload,  Unset):
            payload = UNSET
        else:
            payload = ManagedAgentsAutomationRunDefaultsPayload.from_dict(_payload)




        project_id = d.pop("project_id", UNSET)

        _resources = d.pop("resources", UNSET)
        resources: list[ManagedAgentsSessionResourceRef] | Unset = UNSET
        if _resources is not UNSET:
            resources = []
            for resources_item_data in _resources:
                resources_item = ManagedAgentsSessionResourceRef.from_dict(resources_item_data)



                resources.append(resources_item)


        managed_agents_automation_run_defaults = cls(
            evaluation=evaluation,
            initial_events=initial_events,
            max_cost_usd=max_cost_usd,
            memory_stores=memory_stores,
            metadata=metadata,
            outcome=outcome,
            payload=payload,
            project_id=project_id,
            resources=resources,
        )


        managed_agents_automation_run_defaults.additional_properties = d
        return managed_agents_automation_run_defaults

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
