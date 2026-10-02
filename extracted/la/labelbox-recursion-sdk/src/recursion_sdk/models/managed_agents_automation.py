from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.managed_agents_automation_status import ManagedAgentsAutomationStatus
from ..types import UNSET, Unset
from typing import cast
import datetime

if TYPE_CHECKING:
  from ..models.managed_agents_automation_paused_reason import ManagedAgentsAutomationPausedReason
  from ..models.managed_agents_automation_run_defaults import ManagedAgentsAutomationRunDefaults
  from ..models.managed_agents_automation_trigger import ManagedAgentsAutomationTrigger
  from ..models.managed_agents_vault_credential_ref import ManagedAgentsVaultCredentialRef
  from ..models.managed_agents_webhook_conversation_part import ManagedAgentsWebhookConversationPart
  from ..models.managed_agents_webhook_filter import ManagedAgentsWebhookFilter





T = TypeVar("T", bound="ManagedAgentsAutomation")



@_attrs_define
class ManagedAgentsAutomation:
    """ A provider-neutral rule that starts or continues an ordinary managed-agent session from verified webhook events or
    structured manual input.

        Example:
            {'agent_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'agent_version_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d',
                'archived_at': '2026-02-18T09:30:00Z', 'automation_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d',
                'continue_filter': {'all': [{'operator': 'equals', 'selector': {'body_pointer': 'example', 'header': 'example',
                'source': 'body'}, 'value': 'example', 'values': ['example']}]}, 'conversation_key': [{'selectors':
                [{'body_pointer': 'example', 'header': 'example', 'source': 'body'}]}], 'created_at': '2026-02-18T09:30:00Z',
                'created_by': 'example', 'credential_refs': [{'credential_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d',
                'vault_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d'}], 'display_name': 'example-name', 'enabled': True,
                'environment_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'initial_message': 'example', 'organization_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'paused_reason': {'message': 'example', 'occurred_at':
                '2026-02-18T09:30:00Z', 'paused_by': 'example', 'reason': 'example', 'resource_id':
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
                '2026-02-18T09:30:00Z', 'vault_ids': ['example'], 'webhook_endpoint_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d'}

        Attributes:
            agent_id (str): Managed agent started for each new matching conversation.
            automation_id (str): Server-assigned automation identifier.
            continue_filter (ManagedAgentsWebhookFilter): A conjunction of conditions that decides whether a webhook
                delivery starts or continues an automation conversation. Example: {'all': [{'operator': 'equals', 'selector':
                {'body_pointer': 'example', 'header': 'example', 'source': 'body'}, 'value': 'example', 'values':
                ['example']}]}.
            created_at (datetime.datetime): Server-assigned RFC 3339 creation timestamp.
            display_name (str): Human-readable name shown in the automation catalog and session provenance.
            enabled (bool): Whether this automation may start work. Deprecated projection of status: true means active.
            environment_id (str): Agent Service environment used to run sessions created by this automation.
            initial_message (str): Initial user message for each new session, followed by the trigger context. Scheduled
                runs also include run_defaults.payload when configured.
            organization_id (str): Organization that owns the automation, resolved from the authenticated request scope.
            start_filter (ManagedAgentsWebhookFilter): A conjunction of conditions that decides whether a webhook delivery
                starts or continues an automation conversation. Example: {'all': [{'operator': 'equals', 'selector':
                {'body_pointer': 'example', 'header': 'example', 'source': 'body'}, 'value': 'example', 'values':
                ['example']}]}.
            updated_at (datetime.datetime): Server-assigned RFC 3339 timestamp of the most recent configuration change.
            agent_version_id (str | Unset): Concrete agent version every run uses. Resolved from agent_id at write time and
                echoed back, so a scheduled job's behaviour cannot change underneath it; send it explicitly to pin a specific
                version.
            archived_at (datetime.datetime | Unset): Server-assigned RFC 3339 instant the automation was archived.
            conversation_key (list[ManagedAgentsWebhookConversationPart] | Unset): Ordered values joined into a stable
                external conversation identity; omit to start an independent session per matching delivery. Deprecated: use
                triggers[].webhook.conversation_key.
            created_by (str | Unset): Authenticated principal that created the automation.
            credential_refs (list[ManagedAgentsVaultCredentialRef] | Unset): Explicit credential grants made available to
                automation sessions.
            paused_reason (ManagedAgentsAutomationPausedReason | Unset): Why an automation is not firing, and which resource
                to repair. Example: {'message': 'example', 'occurred_at': '2026-02-18T09:30:00Z', 'paused_by': 'example',
                'reason': 'example', 'resource_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'run_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d'}.
            run_defaults (ManagedAgentsAutomationRunDefaults | Unset): The session shape every run of an automation
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
            status (ManagedAgentsAutomationStatus | Unset): Lifecycle state. archived is terminal. Server-assigned; change
                it through the pause, unpause, and archive operations.
            template_id (str | Unset): Opaque client-owned template identifier used to select a guided editor; unknown
                identifiers remain valid custom automations.
            triggers (list[ManagedAgentsAutomationTrigger] | Unset): Reasons this automation starts work. When present,
                authoritative over the deprecated flat webhook fields.
            vault_ids (list[str] | Unset): Vaults available to automation sessions, further narrowed by credential_refs when
                configured.
            webhook_endpoint_id (str | Unset): Webhook endpoint that supplies automatic events; omit for a manual-only
                automation.
     """

    agent_id: str
    automation_id: str
    continue_filter: ManagedAgentsWebhookFilter
    created_at: datetime.datetime
    display_name: str
    enabled: bool
    environment_id: str
    initial_message: str
    organization_id: str
    start_filter: ManagedAgentsWebhookFilter
    updated_at: datetime.datetime
    agent_version_id: str | Unset = UNSET
    archived_at: datetime.datetime | Unset = UNSET
    conversation_key: list[ManagedAgentsWebhookConversationPart] | Unset = UNSET
    created_by: str | Unset = UNSET
    credential_refs: list[ManagedAgentsVaultCredentialRef] | Unset = UNSET
    paused_reason: ManagedAgentsAutomationPausedReason | Unset = UNSET
    run_defaults: ManagedAgentsAutomationRunDefaults | Unset = UNSET
    status: ManagedAgentsAutomationStatus | Unset = UNSET
    template_id: str | Unset = UNSET
    triggers: list[ManagedAgentsAutomationTrigger] | Unset = UNSET
    vault_ids: list[str] | Unset = UNSET
    webhook_endpoint_id: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.managed_agents_automation_paused_reason import ManagedAgentsAutomationPausedReason # noqa: PLC0415
        from ..models.managed_agents_automation_run_defaults import ManagedAgentsAutomationRunDefaults # noqa: PLC0415
        from ..models.managed_agents_automation_trigger import ManagedAgentsAutomationTrigger # noqa: PLC0415
        from ..models.managed_agents_vault_credential_ref import ManagedAgentsVaultCredentialRef # noqa: PLC0415
        from ..models.managed_agents_webhook_conversation_part import ManagedAgentsWebhookConversationPart # noqa: PLC0415
        from ..models.managed_agents_webhook_filter import ManagedAgentsWebhookFilter # noqa: PLC0415
        agent_id = self.agent_id

        automation_id = self.automation_id

        continue_filter = self.continue_filter.to_dict()

        created_at = self.created_at.isoformat()

        display_name = self.display_name

        enabled = self.enabled

        environment_id = self.environment_id

        initial_message = self.initial_message

        organization_id = self.organization_id

        start_filter = self.start_filter.to_dict()

        updated_at = self.updated_at.isoformat()

        agent_version_id = self.agent_version_id

        archived_at: str | Unset = UNSET
        if not isinstance(self.archived_at, Unset):
            archived_at = self.archived_at.isoformat()

        conversation_key: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.conversation_key, Unset):
            conversation_key = []
            for conversation_key_item_data in self.conversation_key:
                conversation_key_item = conversation_key_item_data.to_dict()
                conversation_key.append(conversation_key_item)



        created_by = self.created_by

        credential_refs: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.credential_refs, Unset):
            credential_refs = []
            for credential_refs_item_data in self.credential_refs:
                credential_refs_item = credential_refs_item_data.to_dict()
                credential_refs.append(credential_refs_item)



        paused_reason: dict[str, Any] | Unset = UNSET
        if not isinstance(self.paused_reason, Unset):
            paused_reason = self.paused_reason.to_dict()

        run_defaults: dict[str, Any] | Unset = UNSET
        if not isinstance(self.run_defaults, Unset):
            run_defaults = self.run_defaults.to_dict()

        status: str | Unset = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.value


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
            "automation_id": automation_id,
            "continue_filter": continue_filter,
            "created_at": created_at,
            "display_name": display_name,
            "enabled": enabled,
            "environment_id": environment_id,
            "initial_message": initial_message,
            "organization_id": organization_id,
            "start_filter": start_filter,
            "updated_at": updated_at,
        })
        if agent_version_id is not UNSET:
            field_dict["agent_version_id"] = agent_version_id
        if archived_at is not UNSET:
            field_dict["archived_at"] = archived_at
        if conversation_key is not UNSET:
            field_dict["conversation_key"] = conversation_key
        if created_by is not UNSET:
            field_dict["created_by"] = created_by
        if credential_refs is not UNSET:
            field_dict["credential_refs"] = credential_refs
        if paused_reason is not UNSET:
            field_dict["paused_reason"] = paused_reason
        if run_defaults is not UNSET:
            field_dict["run_defaults"] = run_defaults
        if status is not UNSET:
            field_dict["status"] = status
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
        from ..models.managed_agents_automation_paused_reason import ManagedAgentsAutomationPausedReason # noqa: PLC0415
        from ..models.managed_agents_automation_run_defaults import ManagedAgentsAutomationRunDefaults # noqa: PLC0415
        from ..models.managed_agents_automation_trigger import ManagedAgentsAutomationTrigger # noqa: PLC0415
        from ..models.managed_agents_vault_credential_ref import ManagedAgentsVaultCredentialRef # noqa: PLC0415
        from ..models.managed_agents_webhook_conversation_part import ManagedAgentsWebhookConversationPart # noqa: PLC0415
        from ..models.managed_agents_webhook_filter import ManagedAgentsWebhookFilter # noqa: PLC0415
        d = dict(src_dict)
        agent_id = d.pop("agent_id")

        automation_id = d.pop("automation_id")

        continue_filter = ManagedAgentsWebhookFilter.from_dict(d.pop("continue_filter"))




        created_at = datetime.datetime.fromisoformat(d.pop("created_at"))




        display_name = d.pop("display_name")

        enabled = d.pop("enabled")

        environment_id = d.pop("environment_id")

        initial_message = d.pop("initial_message")

        organization_id = d.pop("organization_id")

        start_filter = ManagedAgentsWebhookFilter.from_dict(d.pop("start_filter"))




        updated_at = datetime.datetime.fromisoformat(d.pop("updated_at"))




        agent_version_id = d.pop("agent_version_id", UNSET)

        _archived_at = d.pop("archived_at", UNSET)
        archived_at: datetime.datetime | Unset
        if isinstance(_archived_at,  Unset):
            archived_at = UNSET
        else:
            archived_at = datetime.datetime.fromisoformat(_archived_at)




        _conversation_key = d.pop("conversation_key", UNSET)
        conversation_key: list[ManagedAgentsWebhookConversationPart] | Unset = UNSET
        if _conversation_key is not UNSET:
            conversation_key = []
            for conversation_key_item_data in _conversation_key:
                conversation_key_item = ManagedAgentsWebhookConversationPart.from_dict(conversation_key_item_data)



                conversation_key.append(conversation_key_item)


        created_by = d.pop("created_by", UNSET)

        _credential_refs = d.pop("credential_refs", UNSET)
        credential_refs: list[ManagedAgentsVaultCredentialRef] | Unset = UNSET
        if _credential_refs is not UNSET:
            credential_refs = []
            for credential_refs_item_data in _credential_refs:
                credential_refs_item = ManagedAgentsVaultCredentialRef.from_dict(credential_refs_item_data)



                credential_refs.append(credential_refs_item)


        _paused_reason = d.pop("paused_reason", UNSET)
        paused_reason: ManagedAgentsAutomationPausedReason | Unset
        if isinstance(_paused_reason,  Unset):
            paused_reason = UNSET
        else:
            paused_reason = ManagedAgentsAutomationPausedReason.from_dict(_paused_reason)




        _run_defaults = d.pop("run_defaults", UNSET)
        run_defaults: ManagedAgentsAutomationRunDefaults | Unset
        if isinstance(_run_defaults,  Unset):
            run_defaults = UNSET
        else:
            run_defaults = ManagedAgentsAutomationRunDefaults.from_dict(_run_defaults)




        _status = d.pop("status", UNSET)
        status: ManagedAgentsAutomationStatus | Unset
        if isinstance(_status,  Unset):
            status = UNSET
        else:
            status = ManagedAgentsAutomationStatus(_status)




        template_id = d.pop("template_id", UNSET)

        _triggers = d.pop("triggers", UNSET)
        triggers: list[ManagedAgentsAutomationTrigger] | Unset = UNSET
        if _triggers is not UNSET:
            triggers = []
            for triggers_item_data in _triggers:
                triggers_item = ManagedAgentsAutomationTrigger.from_dict(triggers_item_data)



                triggers.append(triggers_item)


        vault_ids = cast(list[str], d.pop("vault_ids", UNSET))


        webhook_endpoint_id = d.pop("webhook_endpoint_id", UNSET)

        managed_agents_automation = cls(
            agent_id=agent_id,
            automation_id=automation_id,
            continue_filter=continue_filter,
            created_at=created_at,
            display_name=display_name,
            enabled=enabled,
            environment_id=environment_id,
            initial_message=initial_message,
            organization_id=organization_id,
            start_filter=start_filter,
            updated_at=updated_at,
            agent_version_id=agent_version_id,
            archived_at=archived_at,
            conversation_key=conversation_key,
            created_by=created_by,
            credential_refs=credential_refs,
            paused_reason=paused_reason,
            run_defaults=run_defaults,
            status=status,
            template_id=template_id,
            triggers=triggers,
            vault_ids=vault_ids,
            webhook_endpoint_id=webhook_endpoint_id,
        )


        managed_agents_automation.additional_properties = d
        return managed_agents_automation

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
