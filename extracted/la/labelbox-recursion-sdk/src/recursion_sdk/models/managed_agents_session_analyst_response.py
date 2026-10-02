from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.managed_agents_session import ManagedAgentsSession





T = TypeVar("T", bound="ManagedAgentsSessionAnalystResponse")



@_attrs_define
class ManagedAgentsSessionAnalystResponse:
    """ Response body of openSessionAnalyst: the caller's read-only analyst session over a session tree, if there is one,
    and whether it was just started.

        Example:
            {'created': True, 'session': {'access_policy': 'admin_only', 'active_handoff': {'access_expires_at':
                '2026-02-18T09:30:00Z', 'deadline_at': '2026-02-18T09:30:00Z', 'handoff_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'reason': 'example', 'requested_at': '2026-02-18T09:30:00Z', 'state':
                'awaiting_user', 'wake_cause': 'example'}, 'agent_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'agent_snapshot':
                {'key': 'example'}, 'agent_version_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'computer_use': True,
                'concurrency_slot_held': True, 'config': {'key': 'example'}, 'created_at': '2026-02-18T09:30:00Z',
                'credential_refs': [{'credential_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'vault_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d'}], 'credential_refs_configured': True, 'effective_model': 'example',
                'environment_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'execution_state': 'provisioning',
                'external_source_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'external_source_type': 'example', 'failure':
                {'at': '2026-02-18T09:30:00Z', 'category': 'transient', 'code': 'example', 'message': 'example', 'phase':
                'example', 'retryable': True}, 'forked_at_event_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'kind': 'api_call',
                'last_activity_at': '2026-02-18T09:30:00Z', 'metadata': {'key': 'example'}, 'model_ref_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'model_snapshot': {'key': 'example'}, 'organization_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'parent_session_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d',
                'project_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'project_source': 'example', 'root_session_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'sandbox_instance_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d',
                'sandbox_provider': 'example', 'session_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'session_path': 'example',
                'source_refs': {'key': 'example'}, 'status': 'active', 'stop_reason': 'example', 'tenant_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'updated_at': '2026-02-18T09:30:00Z', 'user_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'vault_ids': ['example'], 'wake_at': '2026-02-18T09:30:00Z'}}

        Attributes:
            created (bool): True when this call started the analyst; false when it returned the caller's existing
                conversation with this tree, or none.
            session (ManagedAgentsSession | Unset): One durable agent run: its lifecycle status (active, awaiting_human,
                completed, failed, cancelled), the agent version, environment, model, and credentials it was pinned to, and its
                place in a multi-agent tree. Returned when starting, reading, or listing sessions; imported RL rollouts appear
                as sessions too and run no agent loop. Example: {'access_policy': 'admin_only', 'active_handoff':
                {'access_expires_at': '2026-02-18T09:30:00Z', 'deadline_at': '2026-02-18T09:30:00Z', 'handoff_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'reason': 'example', 'requested_at': '2026-02-18T09:30:00Z', 'state':
                'awaiting_user', 'wake_cause': 'example'}, 'agent_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'agent_snapshot':
                {'key': 'example'}, 'agent_version_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'computer_use': True,
                'concurrency_slot_held': True, 'config': {'key': 'example'}, 'created_at': '2026-02-18T09:30:00Z',
                'credential_refs': [{'credential_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'vault_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d'}], 'credential_refs_configured': True, 'effective_model': 'example',
                'environment_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'execution_state': 'provisioning',
                'external_source_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'external_source_type': 'example', 'failure':
                {'at': '2026-02-18T09:30:00Z', 'category': 'transient', 'code': 'example', 'message': 'example', 'phase':
                'example', 'retryable': True}, 'forked_at_event_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'kind': 'api_call',
                'last_activity_at': '2026-02-18T09:30:00Z', 'metadata': {'key': 'example'}, 'model_ref_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'model_snapshot': {'key': 'example'}, 'organization_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'parent_session_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d',
                'project_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'project_source': 'example', 'root_session_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'sandbox_instance_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d',
                'sandbox_provider': 'example', 'session_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'session_path': 'example',
                'source_refs': {'key': 'example'}, 'status': 'active', 'stop_reason': 'example', 'tenant_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'updated_at': '2026-02-18T09:30:00Z', 'user_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'vault_ids': ['example'], 'wake_at': '2026-02-18T09:30:00Z'}.
     """

    created: bool
    session: ManagedAgentsSession | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.managed_agents_session import ManagedAgentsSession # noqa: PLC0415
        created = self.created

        session: dict[str, Any] | Unset = UNSET
        if not isinstance(self.session, Unset):
            session = self.session.to_dict()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "created": created,
        })
        if session is not UNSET:
            field_dict["session"] = session

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.managed_agents_session import ManagedAgentsSession # noqa: PLC0415
        d = dict(src_dict)
        created = d.pop("created")

        _session = d.pop("session", UNSET)
        session: ManagedAgentsSession | Unset
        if isinstance(_session,  Unset):
            session = UNSET
        else:
            session = ManagedAgentsSession.from_dict(_session)




        managed_agents_session_analyst_response = cls(
            created=created,
            session=session,
        )


        managed_agents_session_analyst_response.additional_properties = d
        return managed_agents_session_analyst_response

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
