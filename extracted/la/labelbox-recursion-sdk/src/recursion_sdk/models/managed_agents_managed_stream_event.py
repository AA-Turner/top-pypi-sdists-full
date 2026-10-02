from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.managed_agents_content_block import ManagedAgentsContentBlock
  from ..models.managed_agents_event import ManagedAgentsEvent
  from ..models.managed_agents_managed_stream_event_error import ManagedAgentsManagedStreamEventError
  from ..models.managed_agents_usage import ManagedAgentsUsage





T = TypeVar("T", bound="ManagedAgentsManagedStreamEvent")



@_attrs_define
class ManagedAgentsManagedStreamEvent:
    """ One JSON payload from the managed session event stream. Durable timeline events include their reconnectable id and
    raw event; synthetic lifecycle and error events carry only the applicable compatibility fields.

        Example:
            {'anchor_event_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'content': [{'byte_size': 1, 'content': [],
                'context': 'example', 'data': 'example', 'encrypted_content': 'example', 'height': 1, 'id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'input': {'key': 'example'}, 'is_error': True, 'media_type': 'example',
                'name': 'example-name', 'omitted_bytes': 1, 'payload': 'example', 'provider': 'example', 'provider_payload':
                'example', 'redacted': True, 'semantic_hint': 'example', 'sha256': 'example', 'signature': 'example', 'source':
                {'file_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'type': 'file'}, 'summary': [], 'text': 'example', 'title':
                'example', 'tool_use_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'type': 'example', 'uri': 'example', 'url':
                'https://example.com', 'url_expires_at': '2026-02-18T09:30:00Z', 'width': 1}], 'error': {'key': 'example'},
                'id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'processed_at': '2026-02-18T09:30:00Z', 'raw_event': {'actor':
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
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'turn_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d'}, 'session_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'session_thread_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d',
                'stop_reason': 'example', 'type': 'example', 'usage': {'cache_read_tokens': 1, 'cache_write_tokens': 1,
                'cost_usd': 1.5, 'input_tokens': 1, 'output_tokens': 1}}

        Attributes:
            type_ (str): Managed event type emitted in both the SSE event field and this JSON payload.
            anchor_event_id (str | Unset): Durable event id this event is anchored to, when supplied by event metadata.
            content (list[ManagedAgentsContentBlock] | Unset): Content blocks projected from the durable source event.
            error (ManagedAgentsManagedStreamEventError | Unset): Public failure details for a failed event or session, or
                reconnect guidance after a stream read error.
            id (str | Unset): Durable source event id used as the SSE id and reconnect cursor. Omitted for synthetic status
                and error events.
            processed_at (str | Unset): RFC 3339 timestamp when the durable event was created or the synthetic status event
                was projected.
            raw_event (ManagedAgentsEvent | Unset): One durable entry in a session's transcript: a message, a tool call or
                result, an approval, or a status change, with the provider message body and the token accounting for the call
                that produced it. Returned when listing or streaming a session's events. Example: {'actor': 'human:api',
                'agent_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'cache_read_tokens': 1, 'cache_write_tokens': 1,
                'causal_event_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'content': {'blocks': [{'byte_size': 1, 'content':
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
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'turn_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d'}.
            session_id (str | Unset): Session id associated with the event.
            session_thread_id (str | Unset): Thread id associated with the durable source event.
            stop_reason (Any | Unset): Completion, execution, or session-status reason. Durable events use their string stop
                reason; synthetic status events use an object with a type field.
            usage (ManagedAgentsUsage | Unset): Token counts and cost for a single unit of work, in the provider's usage
                vocabulary. Attached to an event's content for the model turn that produced it; see session usage for whole-
                session totals. Example: {'cache_read_tokens': 1, 'cache_write_tokens': 1, 'cost_usd': 1.5, 'input_tokens': 1,
                'output_tokens': 1}.
     """

    type_: str
    anchor_event_id: str | Unset = UNSET
    content: list[ManagedAgentsContentBlock] | Unset = UNSET
    error: ManagedAgentsManagedStreamEventError | Unset = UNSET
    id: str | Unset = UNSET
    processed_at: str | Unset = UNSET
    raw_event: ManagedAgentsEvent | Unset = UNSET
    session_id: str | Unset = UNSET
    session_thread_id: str | Unset = UNSET
    stop_reason: Any | Unset = UNSET
    usage: ManagedAgentsUsage | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.managed_agents_content_block import ManagedAgentsContentBlock # noqa: PLC0415
        from ..models.managed_agents_event import ManagedAgentsEvent # noqa: PLC0415
        from ..models.managed_agents_managed_stream_event_error import ManagedAgentsManagedStreamEventError # noqa: PLC0415
        from ..models.managed_agents_usage import ManagedAgentsUsage # noqa: PLC0415
        type_ = self.type_

        anchor_event_id = self.anchor_event_id

        content: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.content, Unset):
            content = []
            for content_item_data in self.content:
                content_item = content_item_data.to_dict()
                content.append(content_item)



        error: dict[str, Any] | Unset = UNSET
        if not isinstance(self.error, Unset):
            error = self.error.to_dict()

        id = self.id

        processed_at = self.processed_at

        raw_event: dict[str, Any] | Unset = UNSET
        if not isinstance(self.raw_event, Unset):
            raw_event = self.raw_event.to_dict()

        session_id = self.session_id

        session_thread_id = self.session_thread_id

        stop_reason = self.stop_reason

        usage: dict[str, Any] | Unset = UNSET
        if not isinstance(self.usage, Unset):
            usage = self.usage.to_dict()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "type": type_,
        })
        if anchor_event_id is not UNSET:
            field_dict["anchor_event_id"] = anchor_event_id
        if content is not UNSET:
            field_dict["content"] = content
        if error is not UNSET:
            field_dict["error"] = error
        if id is not UNSET:
            field_dict["id"] = id
        if processed_at is not UNSET:
            field_dict["processed_at"] = processed_at
        if raw_event is not UNSET:
            field_dict["raw_event"] = raw_event
        if session_id is not UNSET:
            field_dict["session_id"] = session_id
        if session_thread_id is not UNSET:
            field_dict["session_thread_id"] = session_thread_id
        if stop_reason is not UNSET:
            field_dict["stop_reason"] = stop_reason
        if usage is not UNSET:
            field_dict["usage"] = usage

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.managed_agents_content_block import ManagedAgentsContentBlock # noqa: PLC0415
        from ..models.managed_agents_event import ManagedAgentsEvent # noqa: PLC0415
        from ..models.managed_agents_managed_stream_event_error import ManagedAgentsManagedStreamEventError # noqa: PLC0415
        from ..models.managed_agents_usage import ManagedAgentsUsage # noqa: PLC0415
        d = dict(src_dict)
        type_ = d.pop("type")

        anchor_event_id = d.pop("anchor_event_id", UNSET)

        _content = d.pop("content", UNSET)
        content: list[ManagedAgentsContentBlock] | Unset = UNSET
        if _content is not UNSET:
            content = []
            for content_item_data in _content:
                content_item = ManagedAgentsContentBlock.from_dict(content_item_data)



                content.append(content_item)


        _error = d.pop("error", UNSET)
        error: ManagedAgentsManagedStreamEventError | Unset
        if isinstance(_error,  Unset):
            error = UNSET
        else:
            error = ManagedAgentsManagedStreamEventError.from_dict(_error)




        id = d.pop("id", UNSET)

        processed_at = d.pop("processed_at", UNSET)

        _raw_event = d.pop("raw_event", UNSET)
        raw_event: ManagedAgentsEvent | Unset
        if isinstance(_raw_event,  Unset):
            raw_event = UNSET
        else:
            raw_event = ManagedAgentsEvent.from_dict(_raw_event)




        session_id = d.pop("session_id", UNSET)

        session_thread_id = d.pop("session_thread_id", UNSET)

        stop_reason = d.pop("stop_reason", UNSET)

        _usage = d.pop("usage", UNSET)
        usage: ManagedAgentsUsage | Unset
        if isinstance(_usage,  Unset):
            usage = UNSET
        else:
            usage = ManagedAgentsUsage.from_dict(_usage)




        managed_agents_managed_stream_event = cls(
            type_=type_,
            anchor_event_id=anchor_event_id,
            content=content,
            error=error,
            id=id,
            processed_at=processed_at,
            raw_event=raw_event,
            session_id=session_id,
            session_thread_id=session_thread_id,
            stop_reason=stop_reason,
            usage=usage,
        )


        managed_agents_managed_stream_event.additional_properties = d
        return managed_agents_managed_stream_event

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
