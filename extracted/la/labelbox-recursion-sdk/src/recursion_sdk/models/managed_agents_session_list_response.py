from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.managed_agents_session_list_item import ManagedAgentsSessionListItem





T = TypeVar("T", bound="ManagedAgentsSessionListResponse")



@_attrs_define
class ManagedAgentsSessionListResponse:
    """ Response body of GET /v1/sessions. Keyset-paginated over (updated_at, id): a page is a stable window at the moment
    it is read, but a session updated between two page reads moves to the front of the list, so a live list may show it
    twice or skip it once. Each row is a summary without the start-time snapshots; read one session for those. Token and
    cost totals are not included; fetch them for a batch of ids via GET /v1/sessions/usage and GET /v1/sessions/costs.

        Example:
            {'next_page_token': 'example', 'sessions': [{'access_policy': 'admin_only', 'active_handoff':
                {'access_expires_at': '2026-02-18T09:30:00Z', 'deadline_at': '2026-02-18T09:30:00Z', 'handoff_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'reason': 'example', 'requested_at': '2026-02-18T09:30:00Z', 'state':
                'awaiting_user', 'wake_cause': 'example'}, 'agent_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'agent_snapshot':
                {'key': 'example'}, 'agent_version_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'computer_use': True,
                'concurrency_slot_held': True, 'config': {'key': 'example'}, 'created_at': '2026-02-18T09:30:00Z',
                'credential_refs': [{'credential_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'vault_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d'}], 'credential_refs_configured': True, 'effective_model': 'example',
                'environment_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'evaluation_eligibility': {'eligible': True, 'reason':
                'not_root', 'snapshot_event_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d'}, 'execution_state': 'provisioning',
                'external_source_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'external_source_type': 'example', 'failure':
                {'at': '2026-02-18T09:30:00Z', 'category': 'transient', 'code': 'example', 'message': 'example', 'phase':
                'example', 'retryable': True}, 'forked_at_event_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'kind': 'api_call',
                'last_activity_at': '2026-02-18T09:30:00Z', 'latest_evaluation': None, 'metadata': {'key': 'example'},
                'model_ref_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'model_snapshot': {'key': 'example'}, 'organization_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'parent_session_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d',
                'project_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'project_source': 'example', 'root_session_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'sandbox_instance_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d',
                'sandbox_provider': 'example', 'session_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'session_path': 'example',
                'source_refs': {'key': 'example'}, 'status': 'active', 'stop_reason': 'example', 'tenant_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'updated_at': '2026-02-18T09:30:00Z', 'user_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'vault_ids': ['example'], 'wake_at': '2026-02-18T09:30:00Z'}]}

        Attributes:
            sessions (list[ManagedAgentsSessionListItem]): Sessions matching the query filters, most recently updated first,
                at most limit (default 100) per page. An empty array means nothing matched. Each public list row includes
                current evaluation eligibility and its newest immutable evaluation, when any. Rows the caller's access policy
                does not permit are dropped silently rather than reported. Rows are summaries: agent_snapshot and model_snapshot
                are omitted and config is an empty object; GET /v1/sessions/{session_id} returns them.
            next_page_token (str | Unset): Present when more sessions match. Pass it as page_token with the same filters and
                limit to read the next page. Absent on the last page.
     """

    sessions: list[ManagedAgentsSessionListItem]
    next_page_token: str | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.managed_agents_session_list_item import ManagedAgentsSessionListItem # noqa: PLC0415
        sessions = []
        for sessions_item_data in self.sessions:
            sessions_item = sessions_item_data.to_dict()
            sessions.append(sessions_item)



        next_page_token = self.next_page_token


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "sessions": sessions,
        })
        if next_page_token is not UNSET:
            field_dict["next_page_token"] = next_page_token

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.managed_agents_session_list_item import ManagedAgentsSessionListItem # noqa: PLC0415
        d = dict(src_dict)
        sessions = []
        _sessions = d.pop("sessions")
        for sessions_item_data in (_sessions):
            sessions_item = ManagedAgentsSessionListItem.from_dict(sessions_item_data)



            sessions.append(sessions_item)


        next_page_token = d.pop("next_page_token", UNSET)

        managed_agents_session_list_response = cls(
            sessions=sessions,
            next_page_token=next_page_token,
        )

        return managed_agents_session_list_response

