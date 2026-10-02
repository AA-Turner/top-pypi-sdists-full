from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.managed_agents_event import ManagedAgentsEvent
  from ..models.managed_agents_session import ManagedAgentsSession
  from ..models.managed_agents_session_thread import ManagedAgentsSessionThread





T = TypeVar("T", bound="ManagedAgentsTreeResult")



@_attrs_define
class ManagedAgentsTreeResult:
    """ A whole multi-agent session tree: every session and thread in it, plus a bounded page of the merged chronological
    event log. Returned when reading the tree containing a given session.

        Example:
            {'events': [{'actor': 'human:api', 'agent_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'cache_read_tokens': 1,
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
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'turn_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d'}], 'next_event_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'root_session_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'sessions':
                [{'access_policy': 'admin_only', 'active_handoff': {'access_expires_at': '2026-02-18T09:30:00Z', 'deadline_at':
                '2026-02-18T09:30:00Z', 'handoff_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'reason': 'example',
                'requested_at': '2026-02-18T09:30:00Z', 'state': 'awaiting_user', 'wake_cause': 'example'}, 'agent_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'agent_snapshot': {'key': 'example'}, 'agent_version_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'computer_use': True, 'concurrency_slot_held': True, 'config': {'key':
                'example'}, 'created_at': '2026-02-18T09:30:00Z', 'credential_refs': [{'credential_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'vault_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d'}],
                'credential_refs_configured': True, 'effective_model': 'example', 'environment_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'execution_state': 'provisioning', 'external_source_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'external_source_type': 'example', 'failure': {'at':
                '2026-02-18T09:30:00Z', 'category': 'transient', 'code': 'example', 'message': 'example', 'phase': 'example',
                'retryable': True}, 'forked_at_event_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'kind': 'api_call',
                'last_activity_at': '2026-02-18T09:30:00Z', 'metadata': {'key': 'example'}, 'model_ref_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'model_snapshot': {'key': 'example'}, 'organization_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'parent_session_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d',
                'project_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'project_source': 'example', 'root_session_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'sandbox_instance_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d',
                'sandbox_provider': 'example', 'session_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'session_path': 'example',
                'source_refs': {'key': 'example'}, 'status': 'active', 'stop_reason': 'example', 'tenant_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'updated_at': '2026-02-18T09:30:00Z', 'user_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'vault_ids': ['example'], 'wake_at': '2026-02-18T09:30:00Z'}],
                'threads': [{'agent_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'agent_version_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'archived_at': '2026-02-18T09:30:00Z', 'created_at':
                '2026-02-18T09:30:00Z', 'name': 'example-name', 'parent_session_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d',
                'parent_thread_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'role': 'user', 'root_session_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'session_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'session_path':
                'example', 'status': 'example', 'stop_reason': {'key': 'example'}, 'thread_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'thread_path': 'example', 'updated_at': '2026-02-18T09:30:00Z'}]}

        Attributes:
            events (list[ManagedAgentsEvent] | None): One page of the tree's events merged into a single chronological log
                across all sessions. Bounded by response size, so the page length is not a fixed count.
            root_session_id (str): Root session of the multi-agent tree this result covers (UUID). Equal to session_id for a
                root session.
            sessions (list[ManagedAgentsSession] | None): Every session in the tree, root and subagents alike. Always
                complete; only the event log is paged.
            threads (list[ManagedAgentsSessionThread] | None): Thread registry rows for the tree's context-isolated
                execution streams. Imported RL children appear when their import supplied thread names; older imports without
                names use session-derived fallback rows.
            next_event_id (str | Unset): Cursor to pass as the starting point of the next event page. Present only when more
                events remain; absent on the last page.
     """

    events: list[ManagedAgentsEvent] | None
    root_session_id: str
    sessions: list[ManagedAgentsSession] | None
    threads: list[ManagedAgentsSessionThread] | None
    next_event_id: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.managed_agents_event import ManagedAgentsEvent # noqa: PLC0415
        from ..models.managed_agents_session import ManagedAgentsSession # noqa: PLC0415
        from ..models.managed_agents_session_thread import ManagedAgentsSessionThread # noqa: PLC0415
        events: list[dict[str, Any]] | None
        if isinstance(self.events, list):
            events = []
            for events_type_0_item_data in self.events:
                events_type_0_item = events_type_0_item_data.to_dict()
                events.append(events_type_0_item)


        else:
            events = self.events

        root_session_id = self.root_session_id

        sessions: list[dict[str, Any]] | None
        if isinstance(self.sessions, list):
            sessions = []
            for sessions_type_0_item_data in self.sessions:
                sessions_type_0_item = sessions_type_0_item_data.to_dict()
                sessions.append(sessions_type_0_item)


        else:
            sessions = self.sessions

        threads: list[dict[str, Any]] | None
        if isinstance(self.threads, list):
            threads = []
            for threads_type_0_item_data in self.threads:
                threads_type_0_item = threads_type_0_item_data.to_dict()
                threads.append(threads_type_0_item)


        else:
            threads = self.threads

        next_event_id = self.next_event_id


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "events": events,
            "root_session_id": root_session_id,
            "sessions": sessions,
            "threads": threads,
        })
        if next_event_id is not UNSET:
            field_dict["next_event_id"] = next_event_id

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.managed_agents_event import ManagedAgentsEvent # noqa: PLC0415
        from ..models.managed_agents_session import ManagedAgentsSession # noqa: PLC0415
        from ..models.managed_agents_session_thread import ManagedAgentsSessionThread # noqa: PLC0415
        d = dict(src_dict)
        def _parse_events(data: object) -> list[ManagedAgentsEvent] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                events_type_0 = []
                _events_type_0 = data
                for events_type_0_item_data in (_events_type_0):
                    events_type_0_item = ManagedAgentsEvent.from_dict(events_type_0_item_data)



                    events_type_0.append(events_type_0_item)

                return events_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[ManagedAgentsEvent] | None, data)

        events = _parse_events(d.pop("events"))


        root_session_id = d.pop("root_session_id")

        def _parse_sessions(data: object) -> list[ManagedAgentsSession] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                sessions_type_0 = []
                _sessions_type_0 = data
                for sessions_type_0_item_data in (_sessions_type_0):
                    sessions_type_0_item = ManagedAgentsSession.from_dict(sessions_type_0_item_data)



                    sessions_type_0.append(sessions_type_0_item)

                return sessions_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[ManagedAgentsSession] | None, data)

        sessions = _parse_sessions(d.pop("sessions"))


        def _parse_threads(data: object) -> list[ManagedAgentsSessionThread] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                threads_type_0 = []
                _threads_type_0 = data
                for threads_type_0_item_data in (_threads_type_0):
                    threads_type_0_item = ManagedAgentsSessionThread.from_dict(threads_type_0_item_data)



                    threads_type_0.append(threads_type_0_item)

                return threads_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[ManagedAgentsSessionThread] | None, data)

        threads = _parse_threads(d.pop("threads"))


        next_event_id = d.pop("next_event_id", UNSET)

        managed_agents_tree_result = cls(
            events=events,
            root_session_id=root_session_id,
            sessions=sessions,
            threads=threads,
            next_event_id=next_event_id,
        )


        managed_agents_tree_result.additional_properties = d
        return managed_agents_tree_result

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
