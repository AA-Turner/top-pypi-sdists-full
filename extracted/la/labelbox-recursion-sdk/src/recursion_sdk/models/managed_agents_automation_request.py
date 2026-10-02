from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.managed_agents_automation_run_defaults_request import ManagedAgentsAutomationRunDefaultsRequest
  from ..models.managed_agents_automation_trigger_request import ManagedAgentsAutomationTriggerRequest
  from ..models.managed_agents_vault_credential_ref_request import ManagedAgentsVaultCredentialRefRequest
  from ..models.managed_agents_webhook_conversation_part_request import ManagedAgentsWebhookConversationPartRequest
  from ..models.managed_agents_webhook_filter_request import ManagedAgentsWebhookFilterRequest





T = TypeVar("T", bound="ManagedAgentsAutomationRequest")



@_attrs_define
class ManagedAgentsAutomationRequest:
    """ Provider-neutral configuration for creating or replacing an automation.

        Example:
            {'agent_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'agent_version_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d',
                'continue_filter': {'all': [{'operator': 'equals', 'selector': {'body_pointer': 'example', 'header': 'example',
                'source': 'body'}, 'value': 'example', 'values': ['example']}]}, 'conversation_key': [{'selectors':
                [{'body_pointer': 'example', 'header': 'example', 'source': 'body'}]}], 'credential_refs': [{'credential_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'vault_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d'}], 'display_name':
                'example-name', 'enabled': True, 'environment_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'initial_message':
                'example', 'run_defaults': {'evaluation': {'limit': 1, 'session_ids': ['example'], 'statuses': ['active']},
                'initial_events': [{'actor': 'human:api', 'agent_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d',
                'cache_read_tokens': 1, 'cache_write_tokens': 1, 'causal_event_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d',
                'content': {'blocks': [{'byte_size': 1, 'content': [], 'context': 'example', 'data': 'example',
                'encrypted_content': 'example', 'height': 1, 'id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'input': {'key':
                'example'}, 'is_error': True, 'media_type': 'example', 'name': 'example-name', 'omitted_bytes': 1, 'payload':
                'example', 'provider': 'example', 'provider_payload': 'example', 'redacted': True, 'semantic_hint': 'example',
                'sha256': 'example', 'signature': 'example', 'source': {'file_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d',
                'type': 'file'}, 'summary': [], 'text': 'example', 'title': 'example', 'tool_use_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'type': 'example', 'uri': 'example', 'url': 'https://example.com',
                'url_expires_at': '2026-02-18T09:30:00Z', 'width': 1}], 'evaluation_budget_reached':
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
                'example', 'header': 'example', 'source': 'body'}, 'value': 'example', 'values': ['example']}]}, 'template_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'triggers': [{'display_name': 'example-name', 'enabled': True,
                'schedule': {'catchup_window_seconds': 1, 'cron': 'example', 'end_at': '2026-02-18T09:30:00Z', 'jitter_seconds':
                1, 'last_run_at': '2026-02-18T09:30:00Z', 'missed_catchup_window': 1, 'next_run_at': '2026-02-18T09:30:00Z',
                'overlap_policy': 'skip', 'skipped_overlap': 1, 'start_at': '2026-02-18T09:30:00Z', 'synchronization': {'error':
                'example', 'status': 'pending'}, 'timezone': 'example', 'upcoming_runs_at': ['2026-02-18T09:30:00Z']},
                'trigger_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'type': 'schedule', 'webhook': {'continue_filter': {'all':
                [{'operator': 'equals', 'selector': {'body_pointer': 'example', 'header': 'example', 'source': 'body'}, 'value':
                'example', 'values': ['example']}]}, 'conversation_key': [{'selectors': [{'body_pointer': 'example', 'header':
                'example', 'source': 'body'}]}], 'start_filter': {'all': [{'operator': 'equals', 'selector': {'body_pointer':
                'example', 'header': 'example', 'source': 'body'}, 'value': 'example', 'values': ['example']}]},
                'webhook_endpoint_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d'}}], 'vault_ids': ['example'],
                'webhook_endpoint_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d'}

        Attributes:
            agent_id (str): Managed agent started for each new matching conversation.
            display_name (str): Human-readable name shown in the automation catalog and session provenance.
            environment_id (str): Agent Service environment used to execute automation sessions.
            initial_message (str): Initial user message for each new session, followed by the trigger context. Scheduled
                runs also include run_defaults.payload when configured.
            agent_version_id (str | Unset): Pin runs to a specific agent version. Omit to pin the agent's current version at
                write time.
            continue_filter (ManagedAgentsWebhookFilterRequest | Unset): A conjunction of conditions that decides whether a
                webhook delivery starts or continues an automation conversation. Example: {'all': [{'operator': 'equals',
                'selector': {'body_pointer': 'example', 'header': 'example', 'source': 'body'}, 'value': 'example', 'values':
                ['example']}]}.
            conversation_key (list[ManagedAgentsWebhookConversationPartRequest] | Unset): Ordered values joined into the
                external conversation identity.
            credential_refs (list[ManagedAgentsVaultCredentialRefRequest] | Unset): Explicit credential grants made
                available to automation sessions.
            enabled (bool | Unset): Deprecated status projection; ignored on writes. New automations start active. Use pause
                and unpause to change lifecycle state.
            run_defaults (ManagedAgentsAutomationRunDefaultsRequest | Unset): The session shape every run of an automation
                produces, copied onto each run rather than shared between them. Example: {'evaluation': {'limit': 1,
                'session_ids': ['example'], 'statuses': ['active']}, 'initial_events': [{'actor': 'human:api', 'agent_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'cache_read_tokens': 1, 'cache_write_tokens': 1, 'causal_event_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'content': {'blocks': [{'byte_size': 1, 'content': [], 'context':
                'example', 'data': 'example', 'encrypted_content': 'example', 'height': 1, 'id':
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
                'mount_path': 'example'}]}.
            start_filter (ManagedAgentsWebhookFilterRequest | Unset): A conjunction of conditions that decides whether a
                webhook delivery starts or continues an automation conversation. Example: {'all': [{'operator': 'equals',
                'selector': {'body_pointer': 'example', 'header': 'example', 'source': 'body'}, 'value': 'example', 'values':
                ['example']}]}.
            template_id (str | Unset): Opaque client-owned template identifier used to select a guided editor; unknown
                identifiers remain valid custom automations.
            triggers (list[ManagedAgentsAutomationTriggerRequest] | Unset): Reasons this automation starts work: schedule,
                webhook, or manual. When present, authoritative over the deprecated flat webhook fields.
            vault_ids (list[str] | Unset): Vaults available to automation sessions, narrowed by credential_refs when
                configured.
            webhook_endpoint_id (str | Unset): Webhook endpoint that supplies automatic events; omit for a manual-only
                automation.
     """

    agent_id: str
    display_name: str
    environment_id: str
    initial_message: str
    agent_version_id: str | Unset = UNSET
    continue_filter: ManagedAgentsWebhookFilterRequest | Unset = UNSET
    conversation_key: list[ManagedAgentsWebhookConversationPartRequest] | Unset = UNSET
    credential_refs: list[ManagedAgentsVaultCredentialRefRequest] | Unset = UNSET
    enabled: bool | Unset = UNSET
    run_defaults: ManagedAgentsAutomationRunDefaultsRequest | Unset = UNSET
    start_filter: ManagedAgentsWebhookFilterRequest | Unset = UNSET
    template_id: str | Unset = UNSET
    triggers: list[ManagedAgentsAutomationTriggerRequest] | Unset = UNSET
    vault_ids: list[str] | Unset = UNSET
    webhook_endpoint_id: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.managed_agents_automation_run_defaults_request import ManagedAgentsAutomationRunDefaultsRequest # noqa: PLC0415
        from ..models.managed_agents_automation_trigger_request import ManagedAgentsAutomationTriggerRequest # noqa: PLC0415
        from ..models.managed_agents_vault_credential_ref_request import ManagedAgentsVaultCredentialRefRequest # noqa: PLC0415
        from ..models.managed_agents_webhook_conversation_part_request import ManagedAgentsWebhookConversationPartRequest # noqa: PLC0415
        from ..models.managed_agents_webhook_filter_request import ManagedAgentsWebhookFilterRequest # noqa: PLC0415
        agent_id = self.agent_id

        display_name = self.display_name

        environment_id = self.environment_id

        initial_message = self.initial_message

        agent_version_id = self.agent_version_id

        continue_filter: dict[str, Any] | Unset = UNSET
        if not isinstance(self.continue_filter, Unset):
            continue_filter = self.continue_filter.to_dict()

        conversation_key: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.conversation_key, Unset):
            conversation_key = []
            for conversation_key_item_data in self.conversation_key:
                conversation_key_item = conversation_key_item_data.to_dict()
                conversation_key.append(conversation_key_item)



        credential_refs: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.credential_refs, Unset):
            credential_refs = []
            for credential_refs_item_data in self.credential_refs:
                credential_refs_item = credential_refs_item_data.to_dict()
                credential_refs.append(credential_refs_item)



        enabled = self.enabled

        run_defaults: dict[str, Any] | Unset = UNSET
        if not isinstance(self.run_defaults, Unset):
            run_defaults = self.run_defaults.to_dict()

        start_filter: dict[str, Any] | Unset = UNSET
        if not isinstance(self.start_filter, Unset):
            start_filter = self.start_filter.to_dict()

        template_id = self.template_id

        triggers: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.triggers, Unset):
            triggers = []
            for triggers_item_data in self.triggers:
                triggers_item = triggers_item_data.to_dict()
                triggers.append(triggers_item)



        vault_ids: list[str] | Unset = UNSET
        if not isinstance(self.vault_ids, Unset):
            vault_ids = self.vault_ids



        webhook_endpoint_id = self.webhook_endpoint_id


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "agent_id": agent_id,
            "display_name": display_name,
            "environment_id": environment_id,
            "initial_message": initial_message,
        })
        if agent_version_id is not UNSET:
            field_dict["agent_version_id"] = agent_version_id
        if continue_filter is not UNSET:
            field_dict["continue_filter"] = continue_filter
        if conversation_key is not UNSET:
            field_dict["conversation_key"] = conversation_key
        if credential_refs is not UNSET:
            field_dict["credential_refs"] = credential_refs
        if enabled is not UNSET:
            field_dict["enabled"] = enabled
        if run_defaults is not UNSET:
            field_dict["run_defaults"] = run_defaults
        if start_filter is not UNSET:
            field_dict["start_filter"] = start_filter
        if template_id is not UNSET:
            field_dict["template_id"] = template_id
        if triggers is not UNSET:
            field_dict["triggers"] = triggers
        if vault_ids is not UNSET:
            field_dict["vault_ids"] = vault_ids
        if webhook_endpoint_id is not UNSET:
            field_dict["webhook_endpoint_id"] = webhook_endpoint_id

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.managed_agents_automation_run_defaults_request import ManagedAgentsAutomationRunDefaultsRequest # noqa: PLC0415
        from ..models.managed_agents_automation_trigger_request import ManagedAgentsAutomationTriggerRequest # noqa: PLC0415
        from ..models.managed_agents_vault_credential_ref_request import ManagedAgentsVaultCredentialRefRequest # noqa: PLC0415
        from ..models.managed_agents_webhook_conversation_part_request import ManagedAgentsWebhookConversationPartRequest # noqa: PLC0415
        from ..models.managed_agents_webhook_filter_request import ManagedAgentsWebhookFilterRequest # noqa: PLC0415
        d = dict(src_dict)
        agent_id = d.pop("agent_id")

        display_name = d.pop("display_name")

        environment_id = d.pop("environment_id")

        initial_message = d.pop("initial_message")

        agent_version_id = d.pop("agent_version_id", UNSET)

        _continue_filter = d.pop("continue_filter", UNSET)
        continue_filter: ManagedAgentsWebhookFilterRequest | Unset
        if isinstance(_continue_filter,  Unset):
            continue_filter = UNSET
        else:
            continue_filter = ManagedAgentsWebhookFilterRequest.from_dict(_continue_filter)




        _conversation_key = d.pop("conversation_key", UNSET)
        conversation_key: list[ManagedAgentsWebhookConversationPartRequest] | Unset = UNSET
        if _conversation_key is not UNSET:
            conversation_key = []
            for conversation_key_item_data in _conversation_key:
                conversation_key_item = ManagedAgentsWebhookConversationPartRequest.from_dict(conversation_key_item_data)



                conversation_key.append(conversation_key_item)


        _credential_refs = d.pop("credential_refs", UNSET)
        credential_refs: list[ManagedAgentsVaultCredentialRefRequest] | Unset = UNSET
        if _credential_refs is not UNSET:
            credential_refs = []
            for credential_refs_item_data in _credential_refs:
                credential_refs_item = ManagedAgentsVaultCredentialRefRequest.from_dict(credential_refs_item_data)



                credential_refs.append(credential_refs_item)


        enabled = d.pop("enabled", UNSET)

        _run_defaults = d.pop("run_defaults", UNSET)
        run_defaults: ManagedAgentsAutomationRunDefaultsRequest | Unset
        if isinstance(_run_defaults,  Unset):
            run_defaults = UNSET
        else:
            run_defaults = ManagedAgentsAutomationRunDefaultsRequest.from_dict(_run_defaults)




        _start_filter = d.pop("start_filter", UNSET)
        start_filter: ManagedAgentsWebhookFilterRequest | Unset
        if isinstance(_start_filter,  Unset):
            start_filter = UNSET
        else:
            start_filter = ManagedAgentsWebhookFilterRequest.from_dict(_start_filter)




        template_id = d.pop("template_id", UNSET)

        _triggers = d.pop("triggers", UNSET)
        triggers: list[ManagedAgentsAutomationTriggerRequest] | Unset = UNSET
        if _triggers is not UNSET:
            triggers = []
            for triggers_item_data in _triggers:
                triggers_item = ManagedAgentsAutomationTriggerRequest.from_dict(triggers_item_data)



                triggers.append(triggers_item)


        vault_ids = cast(list[str], d.pop("vault_ids", UNSET))


        webhook_endpoint_id = d.pop("webhook_endpoint_id", UNSET)

        managed_agents_automation_request = cls(
            agent_id=agent_id,
            display_name=display_name,
            environment_id=environment_id,
            initial_message=initial_message,
            agent_version_id=agent_version_id,
            continue_filter=continue_filter,
            conversation_key=conversation_key,
            credential_refs=credential_refs,
            enabled=enabled,
            run_defaults=run_defaults,
            start_filter=start_filter,
            template_id=template_id,
            triggers=triggers,
            vault_ids=vault_ids,
            webhook_endpoint_id=webhook_endpoint_id,
        )


        managed_agents_automation_request.additional_properties = d
        return managed_agents_automation_request

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
