from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.managed_agents_gestalt_session_row_execution_state import ManagedAgentsGestaltSessionRowExecutionState
from ..models.managed_agents_gestalt_session_row_status import ManagedAgentsGestaltSessionRowStatus
from ..types import UNSET, Unset
from typing import cast
import datetime






T = TypeVar("T", bound="ManagedAgentsGestaltSessionRow")



@_attrs_define
class ManagedAgentsGestaltSessionRow:
    """ One root session as the sessions gestalt projects it: identity, agent, state, and timestamps. Read the session
    itself for anything else.

        Example:
            {'agent_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'created_at': '2026-02-18T09:30:00Z', 'deleted': True,
                'execution_state': 'provisioning', 'failed': True, 'last_activity_at': '2026-02-18T09:30:00Z', 'session_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'status': 'active', 'updated_at': '2026-02-18T09:30:00Z'}

        Attributes:
            created_at (datetime.datetime): RFC 3339 timestamp the session was created at; the gestalt is ordered by it,
                newest first.
            session_id (str): Session id (UUID) of the root session.
            status (ManagedAgentsGestaltSessionRowStatus): Coarse session state, as on the session resource.
            updated_at (datetime.datetime): RFC 3339 timestamp of the row's last change.
            agent_id (str | Unset): Agent the session runs (UUID). Absent for imported sessions that have none.
            deleted (bool | Unset): True on a change-feed row for a session that was deleted since the previous read. Never
                set on a snapshot row.
            execution_state (ManagedAgentsGestaltSessionRowExecutionState | Unset): Where the agent loop is, as on the
                session resource. Absent for sessions without a loop.
            failed (bool | Unset): True when the session carries a terminal failure; GET /v1/sessions/{session_id} has the
                details.
            last_activity_at (datetime.datetime | Unset): RFC 3339 timestamp the agent loop last made progress. Absent for
                sessions that run no loop.
     """

    created_at: datetime.datetime
    session_id: str
    status: ManagedAgentsGestaltSessionRowStatus
    updated_at: datetime.datetime
    agent_id: str | Unset = UNSET
    deleted: bool | Unset = UNSET
    execution_state: ManagedAgentsGestaltSessionRowExecutionState | Unset = UNSET
    failed: bool | Unset = UNSET
    last_activity_at: datetime.datetime | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        created_at = self.created_at.isoformat()

        session_id = self.session_id

        status = self.status.value

        updated_at = self.updated_at.isoformat()

        agent_id = self.agent_id

        deleted = self.deleted

        execution_state: str | Unset = UNSET
        if not isinstance(self.execution_state, Unset):
            execution_state = self.execution_state.value


        failed = self.failed

        last_activity_at: str | Unset = UNSET
        if not isinstance(self.last_activity_at, Unset):
            last_activity_at = self.last_activity_at.isoformat()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "created_at": created_at,
            "session_id": session_id,
            "status": status,
            "updated_at": updated_at,
        })
        if agent_id is not UNSET:
            field_dict["agent_id"] = agent_id
        if deleted is not UNSET:
            field_dict["deleted"] = deleted
        if execution_state is not UNSET:
            field_dict["execution_state"] = execution_state
        if failed is not UNSET:
            field_dict["failed"] = failed
        if last_activity_at is not UNSET:
            field_dict["last_activity_at"] = last_activity_at

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        created_at = datetime.datetime.fromisoformat(d.pop("created_at"))




        session_id = d.pop("session_id")

        status = ManagedAgentsGestaltSessionRowStatus(d.pop("status"))




        updated_at = datetime.datetime.fromisoformat(d.pop("updated_at"))




        agent_id = d.pop("agent_id", UNSET)

        deleted = d.pop("deleted", UNSET)

        _execution_state = d.pop("execution_state", UNSET)
        execution_state: ManagedAgentsGestaltSessionRowExecutionState | Unset
        if isinstance(_execution_state,  Unset):
            execution_state = UNSET
        else:
            execution_state = ManagedAgentsGestaltSessionRowExecutionState(_execution_state)




        failed = d.pop("failed", UNSET)

        _last_activity_at = d.pop("last_activity_at", UNSET)
        last_activity_at: datetime.datetime | Unset
        if isinstance(_last_activity_at,  Unset):
            last_activity_at = UNSET
        else:
            last_activity_at = datetime.datetime.fromisoformat(_last_activity_at)




        managed_agents_gestalt_session_row = cls(
            created_at=created_at,
            session_id=session_id,
            status=status,
            updated_at=updated_at,
            agent_id=agent_id,
            deleted=deleted,
            execution_state=execution_state,
            failed=failed,
            last_activity_at=last_activity_at,
        )


        managed_agents_gestalt_session_row.additional_properties = d
        return managed_agents_gestalt_session_row

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
