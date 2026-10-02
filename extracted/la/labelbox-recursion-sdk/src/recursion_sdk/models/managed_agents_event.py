from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.managed_agents_event_content_hydration_status import ManagedAgentsEventContentHydrationStatus
from ..types import UNSET, Unset
from typing import cast
import datetime

if TYPE_CHECKING:
  from ..models.managed_agents_event_content import ManagedAgentsEventContent
  from ..models.managed_agents_inference_config import ManagedAgentsInferenceConfig
  from ..models.managed_agents_model_ref import ManagedAgentsModelRef





T = TypeVar("T", bound="ManagedAgentsEvent")



@_attrs_define
class ManagedAgentsEvent:
    """ One durable entry in a session's transcript: a message, a tool call or result, an approval, or a status change, with
    the provider message body and the token accounting for the call that produced it. Returned when listing or streaming
    a session's events.

        Example:
            {'actor': 'human:api', 'agent_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'cache_read_tokens': 1,
                'cache_write_tokens': 1, 'causal_event_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'content': {'blocks':
                [{'byte_size': 1, 'content': [], 'context': 'example', 'data': 'example', 'encrypted_content': 'example',
                'height': 1, 'id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'input': {'key': 'example'}, 'is_error': True,
                'media_type': 'example', 'name': 'example-name', 'omitted_bytes': 1, 'payload': 'example', 'provider':
                'example', 'provider_payload': 'example', 'redacted': True, 'semantic_hint': 'example', 'sha256': 'example',
                'signature': 'example', 'source': {'file_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'type': 'file'},
                'summary': [], 'text': 'example', 'title': 'example', 'tool_use_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d',
                'type': 'example', 'uri': 'example', 'url': 'https://example.com', 'url_expires_at': '2026-02-18T09:30:00Z',
                'width': 1}], 'evaluation_budget_reached': {'affected_target_session_ids':
                ['9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d'], 'max_tree_cost_usd': 'example'}, 'evaluation_plan_frozen':
                {'criteria': [{'criterion_key': 'example', 'criterion_text': 'example'}], 'max_concurrent_threads': 1,
                'max_tree_cost_usd': 'example', 'targets': [{'snapshot_event_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d',
                'target_session_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d'}]}, 'evaluation_run_finished': {'failure_code':
                'plan_failed', 'failure_message': 'example', 'targets_budget_reached': 1, 'targets_skipped': 1, 'targets_total':
                1, 'terminal_status': 'completed', 'verdicts_recorded': 1}, 'evaluation_target_skipped': {'child_session_id':
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
                'cost_micros': 1, 'created_at': '2026-02-18T09:30:00Z', 'environment_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'event_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'event_status':
                'example', 'event_type': 'example', 'finish_reason': 'example', 'inference_config': {'max_tokens': 1,
                'provider_params': {'key': 'example'}, 'reasoning_effort': 'example', 'temperature': 1.5, 'top_p': 1.5},
                'input_tokens': 1, 'latency_ms': 1, 'model': {'base_url': 'https://example.com', 'capabilities': {'key':
                'example'}, 'context_window': 1, 'max_output_tokens': 1, 'metadata': {'key': 'example'}, 'model': 'example',
                'model_ref_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'model_version': 'example', 'provider': 'example',
                'provider_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'provider_type': 'example', 'serving_backend':
                'example'}, 'model_ref_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'organization_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'output_tokens': 1, 'parent_event_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'prompt_tokens': 1, 'provider_model_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'provider_request_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d',
                'provider_type': 'example', 'role': 'user', 'sandbox_instance_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d',
                'schema_version': 1, 'session_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'thread_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'tool_name': 'example', 'tool_use_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'turn_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d'}

        Attributes:
            actor (str): Who produced this event, as a namespaced identifier such as human:api, system:api, or an agent
                identity.
            content (ManagedAgentsEventContent): The body of a session event, shaped like a provider message: content blocks
                plus the stop reason and token usage the provider returned. Every event in a session transcript carries one.
                Example: {'blocks': [{'byte_size': 1, 'content': [], 'context': 'example', 'data': 'example',
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
                1.5, 'input_tokens': 1, 'output_tokens': 1}}.
            created_at (datetime.datetime): RFC 3339 timestamp of when this record was created. Server-assigned.
            event_id (str): Identifier for this event (UUID). Server-assigned unless the append supplied one.
                Chronologically sortable, and the column a transcript is ordered by.
            event_type (str): What kind of event this is. One of message, tool_invocation, tool_result, approval_request,
                approval_decision, summary, plan_update, session_status, artifact, advisor_intervention, or outcome_evaluation.
            inference_config (ManagedAgentsInferenceConfig): Sampling and generation settings for a model call, mirroring
                the provider's own request parameters. Set it on an agent or a session to govern every turn, and read it back on
                a model event to see what the call actually used. Example: {'max_tokens': 1, 'provider_params': {'key':
                'example'}, 'reasoning_effort': 'example', 'temperature': 1.5, 'top_p': 1.5}.
            schema_version (int): Event schema version this row was written under. Server-assigned; readers should tolerate
                unknown newer values.
            session_id (str): Session this event belongs to (UUID).
            agent_id (str | Unset): Agent that produced this event (UUID).
            cache_read_tokens (int | Unset): Prompt tokens served from the provider's prompt cache, billed at the cached
                rate.
            cache_write_tokens (int | Unset): Prompt tokens written into the provider's prompt cache.
            causal_event_id (str | Unset): Event that caused this one (UUID). Unlike parent_event_id this expresses
                causality rather than nesting.
            content_hydration_status (ManagedAgentsEventContentHydrationStatus | Unset): Read-time status when external
                EventContent was hydrated or could not be hydrated.
            content_payload_bytes (int | Unset): Byte size of the canonical external EventContent JSON.
            content_payload_ref (str | Unset): Private whole-event JSON reference. Resolve through authenticated APIs; never
                fetch this gs:// URI directly.
            content_payload_sha256 (str | Unset): Lowercase SHA-256 digest of the canonical external EventContent JSON.
            content_ref (str | Unset): Image cleanup prefix or typed multi-image envelope. This is independent of whole-
                event payload storage.
            cost_micros (int | Unset): Accrued cost in micro-USD (1,000,000 = 1 USD). Integer to avoid float rounding across
                many small charges.
            environment_id (str | Unset): Sandbox environment the producing session was executing in (UUID).
            event_status (str | Unset): Outcome marker for events that can fail: pending, completed, warning, or error.
                Empty when not applicable.
            finish_reason (str | Unset): Why the provider stopped generating, in the provider vocabulary (for example
                end_turn, max_tokens, tool_use). Passed through verbatim.
            input_tokens (int | Unset): Prompt tokens billed for this unit of work.
            latency_ms (int | Unset): Wall-clock duration of the provider call in milliseconds.
            model (ManagedAgentsModelRef | Unset): Snapshot of the model that served one inference call, recorded on the
                event so a transcript stays interpretable after the catalog entry changes. Returned on model events; also
                accepted when pinning a session to a specific model. Example: {'base_url': 'https://example.com',
                'capabilities': {'key': 'example'}, 'context_window': 1, 'max_output_tokens': 1, 'metadata': {'key': 'example'},
                'model': 'example', 'model_ref_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'model_version': 'example',
                'provider': 'example', 'provider_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'provider_type': 'example',
                'serving_backend': 'example'}.
            model_ref_id (str | Unset): Canonical model reference used for this inference (UUID). Empty on events not
                produced by a model call.
            organization_id (str | Unset): Organization that owns this record. Resolved from the API key; never accepted
                from the caller.
            output_tokens (int | Unset): Completion tokens billed for this unit of work.
            parent_event_id (str | Unset): Event this one is nested under in the transcript tree (UUID), for example a tool
                result under its invocation.
            prompt_tokens (int | Unset): Estimated tokens this event contributes when rendered into a future provider
                request. A memoized estimate for context-budget planning, not billed provider usage.
            provider_model_id (str | Unset): Provider's own model identifier as sent on the wire, which may differ from the
                canonical model reference.
            provider_request_id (str | Unset): Provider's request identifier for this inference, for correlating with
                provider-side logs.
            provider_type (str | Unset): Model provider family that served this inference, for example anthropic, openai, or
                vertex.
            role (str | Unset): Message role in the provider vocabulary: system, user, or assistant. Set on message events;
                empty on events that are not turns.
            sandbox_instance_id (str | Unset): Concrete sandbox instance the event was produced on. Provider-assigned, not a
                UUID.
            thread_id (str | Unset): Thread within a multi-agent session that produced this event (UUID). Empty on a single-
                agent session.
            tool_name (str | Unset): Name of the tool being invoked or reporting a result. Set on tool events only.
            tool_use_id (str | Unset): Provider's tool-call identifier, correlating a tool_invocation with its tool_result.
            turn_id (str | Unset): Groups every event produced within one model turn.
     """

    actor: str
    content: ManagedAgentsEventContent
    created_at: datetime.datetime
    event_id: str
    event_type: str
    inference_config: ManagedAgentsInferenceConfig
    schema_version: int
    session_id: str
    agent_id: str | Unset = UNSET
    cache_read_tokens: int | Unset = UNSET
    cache_write_tokens: int | Unset = UNSET
    causal_event_id: str | Unset = UNSET
    content_hydration_status: ManagedAgentsEventContentHydrationStatus | Unset = UNSET
    content_payload_bytes: int | Unset = UNSET
    content_payload_ref: str | Unset = UNSET
    content_payload_sha256: str | Unset = UNSET
    content_ref: str | Unset = UNSET
    cost_micros: int | Unset = UNSET
    environment_id: str | Unset = UNSET
    event_status: str | Unset = UNSET
    finish_reason: str | Unset = UNSET
    input_tokens: int | Unset = UNSET
    latency_ms: int | Unset = UNSET
    model: ManagedAgentsModelRef | Unset = UNSET
    model_ref_id: str | Unset = UNSET
    organization_id: str | Unset = UNSET
    output_tokens: int | Unset = UNSET
    parent_event_id: str | Unset = UNSET
    prompt_tokens: int | Unset = UNSET
    provider_model_id: str | Unset = UNSET
    provider_request_id: str | Unset = UNSET
    provider_type: str | Unset = UNSET
    role: str | Unset = UNSET
    sandbox_instance_id: str | Unset = UNSET
    thread_id: str | Unset = UNSET
    tool_name: str | Unset = UNSET
    tool_use_id: str | Unset = UNSET
    turn_id: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.managed_agents_event_content import ManagedAgentsEventContent # noqa: PLC0415
        from ..models.managed_agents_inference_config import ManagedAgentsInferenceConfig # noqa: PLC0415
        from ..models.managed_agents_model_ref import ManagedAgentsModelRef # noqa: PLC0415
        actor = self.actor

        content = self.content.to_dict()

        created_at = self.created_at.isoformat()

        event_id = self.event_id

        event_type = self.event_type

        inference_config = self.inference_config.to_dict()

        schema_version = self.schema_version

        session_id = self.session_id

        agent_id = self.agent_id

        cache_read_tokens = self.cache_read_tokens

        cache_write_tokens = self.cache_write_tokens

        causal_event_id = self.causal_event_id

        content_hydration_status: str | Unset = UNSET
        if not isinstance(self.content_hydration_status, Unset):
            content_hydration_status = self.content_hydration_status.value


        content_payload_bytes = self.content_payload_bytes

        content_payload_ref = self.content_payload_ref

        content_payload_sha256 = self.content_payload_sha256

        content_ref = self.content_ref

        cost_micros = self.cost_micros

        environment_id = self.environment_id

        event_status = self.event_status

        finish_reason = self.finish_reason

        input_tokens = self.input_tokens

        latency_ms = self.latency_ms

        model: dict[str, Any] | Unset = UNSET
        if not isinstance(self.model, Unset):
            model = self.model.to_dict()

        model_ref_id = self.model_ref_id

        organization_id = self.organization_id

        output_tokens = self.output_tokens

        parent_event_id = self.parent_event_id

        prompt_tokens = self.prompt_tokens

        provider_model_id = self.provider_model_id

        provider_request_id = self.provider_request_id

        provider_type = self.provider_type

        role = self.role

        sandbox_instance_id = self.sandbox_instance_id

        thread_id = self.thread_id

        tool_name = self.tool_name

        tool_use_id = self.tool_use_id

        turn_id = self.turn_id


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "actor": actor,
            "content": content,
            "created_at": created_at,
            "event_id": event_id,
            "event_type": event_type,
            "inference_config": inference_config,
            "schema_version": schema_version,
            "session_id": session_id,
        })
        if agent_id is not UNSET:
            field_dict["agent_id"] = agent_id
        if cache_read_tokens is not UNSET:
            field_dict["cache_read_tokens"] = cache_read_tokens
        if cache_write_tokens is not UNSET:
            field_dict["cache_write_tokens"] = cache_write_tokens
        if causal_event_id is not UNSET:
            field_dict["causal_event_id"] = causal_event_id
        if content_hydration_status is not UNSET:
            field_dict["content_hydration_status"] = content_hydration_status
        if content_payload_bytes is not UNSET:
            field_dict["content_payload_bytes"] = content_payload_bytes
        if content_payload_ref is not UNSET:
            field_dict["content_payload_ref"] = content_payload_ref
        if content_payload_sha256 is not UNSET:
            field_dict["content_payload_sha256"] = content_payload_sha256
        if content_ref is not UNSET:
            field_dict["content_ref"] = content_ref
        if cost_micros is not UNSET:
            field_dict["cost_micros"] = cost_micros
        if environment_id is not UNSET:
            field_dict["environment_id"] = environment_id
        if event_status is not UNSET:
            field_dict["event_status"] = event_status
        if finish_reason is not UNSET:
            field_dict["finish_reason"] = finish_reason
        if input_tokens is not UNSET:
            field_dict["input_tokens"] = input_tokens
        if latency_ms is not UNSET:
            field_dict["latency_ms"] = latency_ms
        if model is not UNSET:
            field_dict["model"] = model
        if model_ref_id is not UNSET:
            field_dict["model_ref_id"] = model_ref_id
        if organization_id is not UNSET:
            field_dict["organization_id"] = organization_id
        if output_tokens is not UNSET:
            field_dict["output_tokens"] = output_tokens
        if parent_event_id is not UNSET:
            field_dict["parent_event_id"] = parent_event_id
        if prompt_tokens is not UNSET:
            field_dict["prompt_tokens"] = prompt_tokens
        if provider_model_id is not UNSET:
            field_dict["provider_model_id"] = provider_model_id
        if provider_request_id is not UNSET:
            field_dict["provider_request_id"] = provider_request_id
        if provider_type is not UNSET:
            field_dict["provider_type"] = provider_type
        if role is not UNSET:
            field_dict["role"] = role
        if sandbox_instance_id is not UNSET:
            field_dict["sandbox_instance_id"] = sandbox_instance_id
        if thread_id is not UNSET:
            field_dict["thread_id"] = thread_id
        if tool_name is not UNSET:
            field_dict["tool_name"] = tool_name
        if tool_use_id is not UNSET:
            field_dict["tool_use_id"] = tool_use_id
        if turn_id is not UNSET:
            field_dict["turn_id"] = turn_id

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.managed_agents_event_content import ManagedAgentsEventContent # noqa: PLC0415
        from ..models.managed_agents_inference_config import ManagedAgentsInferenceConfig # noqa: PLC0415
        from ..models.managed_agents_model_ref import ManagedAgentsModelRef # noqa: PLC0415
        d = dict(src_dict)
        actor = d.pop("actor")

        content = ManagedAgentsEventContent.from_dict(d.pop("content"))




        created_at = datetime.datetime.fromisoformat(d.pop("created_at"))




        event_id = d.pop("event_id")

        event_type = d.pop("event_type")

        inference_config = ManagedAgentsInferenceConfig.from_dict(d.pop("inference_config"))




        schema_version = d.pop("schema_version")

        session_id = d.pop("session_id")

        agent_id = d.pop("agent_id", UNSET)

        cache_read_tokens = d.pop("cache_read_tokens", UNSET)

        cache_write_tokens = d.pop("cache_write_tokens", UNSET)

        causal_event_id = d.pop("causal_event_id", UNSET)

        _content_hydration_status = d.pop("content_hydration_status", UNSET)
        content_hydration_status: ManagedAgentsEventContentHydrationStatus | Unset
        if isinstance(_content_hydration_status,  Unset):
            content_hydration_status = UNSET
        else:
            content_hydration_status = ManagedAgentsEventContentHydrationStatus(_content_hydration_status)




        content_payload_bytes = d.pop("content_payload_bytes", UNSET)

        content_payload_ref = d.pop("content_payload_ref", UNSET)

        content_payload_sha256 = d.pop("content_payload_sha256", UNSET)

        content_ref = d.pop("content_ref", UNSET)

        cost_micros = d.pop("cost_micros", UNSET)

        environment_id = d.pop("environment_id", UNSET)

        event_status = d.pop("event_status", UNSET)

        finish_reason = d.pop("finish_reason", UNSET)

        input_tokens = d.pop("input_tokens", UNSET)

        latency_ms = d.pop("latency_ms", UNSET)

        _model = d.pop("model", UNSET)
        model: ManagedAgentsModelRef | Unset
        if isinstance(_model,  Unset):
            model = UNSET
        else:
            model = ManagedAgentsModelRef.from_dict(_model)




        model_ref_id = d.pop("model_ref_id", UNSET)

        organization_id = d.pop("organization_id", UNSET)

        output_tokens = d.pop("output_tokens", UNSET)

        parent_event_id = d.pop("parent_event_id", UNSET)

        prompt_tokens = d.pop("prompt_tokens", UNSET)

        provider_model_id = d.pop("provider_model_id", UNSET)

        provider_request_id = d.pop("provider_request_id", UNSET)

        provider_type = d.pop("provider_type", UNSET)

        role = d.pop("role", UNSET)

        sandbox_instance_id = d.pop("sandbox_instance_id", UNSET)

        thread_id = d.pop("thread_id", UNSET)

        tool_name = d.pop("tool_name", UNSET)

        tool_use_id = d.pop("tool_use_id", UNSET)

        turn_id = d.pop("turn_id", UNSET)

        managed_agents_event = cls(
            actor=actor,
            content=content,
            created_at=created_at,
            event_id=event_id,
            event_type=event_type,
            inference_config=inference_config,
            schema_version=schema_version,
            session_id=session_id,
            agent_id=agent_id,
            cache_read_tokens=cache_read_tokens,
            cache_write_tokens=cache_write_tokens,
            causal_event_id=causal_event_id,
            content_hydration_status=content_hydration_status,
            content_payload_bytes=content_payload_bytes,
            content_payload_ref=content_payload_ref,
            content_payload_sha256=content_payload_sha256,
            content_ref=content_ref,
            cost_micros=cost_micros,
            environment_id=environment_id,
            event_status=event_status,
            finish_reason=finish_reason,
            input_tokens=input_tokens,
            latency_ms=latency_ms,
            model=model,
            model_ref_id=model_ref_id,
            organization_id=organization_id,
            output_tokens=output_tokens,
            parent_event_id=parent_event_id,
            prompt_tokens=prompt_tokens,
            provider_model_id=provider_model_id,
            provider_request_id=provider_request_id,
            provider_type=provider_type,
            role=role,
            sandbox_instance_id=sandbox_instance_id,
            thread_id=thread_id,
            tool_name=tool_name,
            tool_use_id=tool_use_id,
            turn_id=turn_id,
        )


        managed_agents_event.additional_properties = d
        return managed_agents_event

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
