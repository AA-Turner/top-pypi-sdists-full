from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.managed_agents_automation import ManagedAgentsAutomation





T = TypeVar("T", bound="ManagedAgentsAutomationListResponse")



@_attrs_define
class ManagedAgentsAutomationListResponse:
    """ Automations available in the calling organization.

        Example:
            {'automations': [{'agent_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'agent_version_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'archived_at': '2026-02-18T09:30:00Z', 'automation_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'continue_filter': {'all': [{'operator': 'equals', 'selector':
                {'body_pointer': 'example', 'header': 'example', 'source': 'body'}, 'value': 'example', 'values':
                ['example']}]}, 'conversation_key': [{'selectors': [{'body_pointer': 'example', 'header': 'example', 'source':
                'body'}]}], 'created_at': '2026-02-18T09:30:00Z', 'created_by': 'example', 'credential_refs': [{'credential_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'vault_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d'}], 'display_name':
                'example-name', 'enabled': True, 'environment_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'initial_message':
                'example', 'organization_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'paused_reason': {'message': 'example',
                'occurred_at': '2026-02-18T09:30:00Z', 'paused_by': 'example', 'reason': 'example', 'resource_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'run_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d'}, 'run_defaults':
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
                'mount_path': 'example'}]}, 'start_filter': {'all': [{'operator': 'equals', 'selector': {'body_pointer':
                'example', 'header': 'example', 'source': 'body'}, 'value': 'example', 'values': ['example']}]}, 'status':
                'active', 'template_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'triggers': [{'display_name': 'example-name',
                'enabled': True, 'schedule': {'catchup_window_seconds': 1, 'cron': 'example', 'end_at': '2026-02-18T09:30:00Z',
                'jitter_seconds': 1, 'last_run_at': '2026-02-18T09:30:00Z', 'missed_catchup_window': 1, 'next_run_at':
                '2026-02-18T09:30:00Z', 'overlap_policy': 'skip', 'skipped_overlap': 1, 'start_at': '2026-02-18T09:30:00Z',
                'synchronization': {'error': 'example', 'status': 'pending'}, 'timezone': 'example', 'upcoming_runs_at':
                ['2026-02-18T09:30:00Z']}, 'trigger_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'type': 'schedule', 'webhook':
                {'continue_filter': {'all': [{'operator': 'equals', 'selector': {'body_pointer': 'example', 'header': 'example',
                'source': 'body'}, 'value': 'example', 'values': ['example']}]}, 'conversation_key': [{'selectors':
                [{'body_pointer': 'example', 'header': 'example', 'source': 'body'}]}], 'start_filter': {'all': [{'operator':
                'equals', 'selector': {'body_pointer': 'example', 'header': 'example', 'source': 'body'}, 'value': 'example',
                'values': ['example']}]}, 'webhook_endpoint_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d'}}], 'updated_at':
                '2026-02-18T09:30:00Z', 'vault_ids': ['example'], 'webhook_endpoint_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d'}]}

        Attributes:
            automations (list[ManagedAgentsAutomation] | None): Automations owned by the calling organization.
     """

    automations: list[ManagedAgentsAutomation] | None
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.managed_agents_automation import ManagedAgentsAutomation # noqa: PLC0415
        automations: list[dict[str, Any]] | None
        if isinstance(self.automations, list):
            automations = []
            for automations_type_0_item_data in self.automations:
                automations_type_0_item = automations_type_0_item_data.to_dict()
                automations.append(automations_type_0_item)


        else:
            automations = self.automations


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "automations": automations,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.managed_agents_automation import ManagedAgentsAutomation # noqa: PLC0415
        d = dict(src_dict)
        def _parse_automations(data: object) -> list[ManagedAgentsAutomation] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                automations_type_0 = []
                _automations_type_0 = data
                for automations_type_0_item_data in (_automations_type_0):
                    automations_type_0_item = ManagedAgentsAutomation.from_dict(automations_type_0_item_data)



                    automations_type_0.append(automations_type_0_item)

                return automations_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[ManagedAgentsAutomation] | None, data)

        automations = _parse_automations(d.pop("automations"))


        managed_agents_automation_list_response = cls(
            automations=automations,
        )


        managed_agents_automation_list_response.additional_properties = d
        return managed_agents_automation_list_response

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
