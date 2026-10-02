from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast
import datetime

if TYPE_CHECKING:
  from ..models.managed_agents_session_thread_stop_reason import ManagedAgentsSessionThreadStopReason





T = TypeVar("T", bound="ManagedAgentsSessionThread")



@_attrs_define
class ManagedAgentsSessionThread:
    """ One context-isolated execution stream inside a multi-agent session tree, as registered in the thread registry.
    Returned when listing a session's threads or reading a whole session tree.

        Example:
            {'agent_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'agent_version_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d',
                'archived_at': '2026-02-18T09:30:00Z', 'created_at': '2026-02-18T09:30:00Z', 'name': 'example-name',
                'parent_session_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'parent_thread_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'role': 'user', 'root_session_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'session_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'session_path':
                'example', 'status': 'example', 'stop_reason': {'key': 'example'}, 'thread_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'thread_path': 'example', 'updated_at': '2026-02-18T09:30:00Z'}

        Attributes:
            agent_id (str): Agent this thread runs (UUID).
            created_at (datetime.datetime): RFC 3339 timestamp of when this record was created. Server-assigned.
            role (str): What the thread exists to do within the tree, for example subagent, grader, or advisor. Not a chat
                message role.
            root_session_id (str): Root session of the multi-agent tree this thread belongs to (UUID). Equal to session_id
                for a root session.
            session_id (str): Session this thread belongs to (UUID).
            session_path (str): Slash-joined ancestry of session ids from the tree root down to the session whose events
                this thread's events are stored under, for example "/root-id/child-id".
            status (str): Thread lifecycle: running (executing now), idle (awaiting more input), or terminated (finished;
                see stop_reason).
            thread_id (str): Identifier for this thread within its session tree (UUID). Server-assigned. For a subagent
                thread it is the child session id, so the thread and the session carrying its events resolve each other
                directly.
            thread_path (str): Slash-joined ancestry of this thread within the tree, used to order threads for display.
                Defaults to session_path when the thread has no deeper nesting of its own.
            updated_at (datetime.datetime): RFC 3339 timestamp of the last change to this record. Server-assigned.
            agent_version_id (str | Unset): Agent version this thread runs (UUID). Absent when the thread was not pinned to
                a specific version.
            archived_at (datetime.datetime | Unset): RFC 3339 timestamp of when this thread was archived and stopped
                appearing as an active stream. Absent while the thread is not archived.
            name (str | Unset): Human-readable label for this thread, supplied when it was spawned. Optional and never
                interpreted by the service.
            parent_session_id (str | Unset): Session the spawning thread belongs to (UUID). Absent on the tree's top-level
                thread.
            parent_thread_id (str | Unset): Thread that spawned this one (UUID). Absent on the tree's top-level thread.
            stop_reason (ManagedAgentsSessionThreadStopReason | Unset): Structured reason the thread last stopped, forwarded
                from the agent loop, for example {"type": "end_turn"} or {"type": "error", "message": ...}. Absent while the
                thread has not stopped.
     """

    agent_id: str
    created_at: datetime.datetime
    role: str
    root_session_id: str
    session_id: str
    session_path: str
    status: str
    thread_id: str
    thread_path: str
    updated_at: datetime.datetime
    agent_version_id: str | Unset = UNSET
    archived_at: datetime.datetime | Unset = UNSET
    name: str | Unset = UNSET
    parent_session_id: str | Unset = UNSET
    parent_thread_id: str | Unset = UNSET
    stop_reason: ManagedAgentsSessionThreadStopReason | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.managed_agents_session_thread_stop_reason import ManagedAgentsSessionThreadStopReason # noqa: PLC0415
        agent_id = self.agent_id

        created_at = self.created_at.isoformat()

        role = self.role

        root_session_id = self.root_session_id

        session_id = self.session_id

        session_path = self.session_path

        status = self.status

        thread_id = self.thread_id

        thread_path = self.thread_path

        updated_at = self.updated_at.isoformat()

        agent_version_id = self.agent_version_id

        archived_at: str | Unset = UNSET
        if not isinstance(self.archived_at, Unset):
            archived_at = self.archived_at.isoformat()

        name = self.name

        parent_session_id = self.parent_session_id

        parent_thread_id = self.parent_thread_id

        stop_reason: dict[str, Any] | Unset = UNSET
        if not isinstance(self.stop_reason, Unset):
            stop_reason = self.stop_reason.to_dict()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "agent_id": agent_id,
            "created_at": created_at,
            "role": role,
            "root_session_id": root_session_id,
            "session_id": session_id,
            "session_path": session_path,
            "status": status,
            "thread_id": thread_id,
            "thread_path": thread_path,
            "updated_at": updated_at,
        })
        if agent_version_id is not UNSET:
            field_dict["agent_version_id"] = agent_version_id
        if archived_at is not UNSET:
            field_dict["archived_at"] = archived_at
        if name is not UNSET:
            field_dict["name"] = name
        if parent_session_id is not UNSET:
            field_dict["parent_session_id"] = parent_session_id
        if parent_thread_id is not UNSET:
            field_dict["parent_thread_id"] = parent_thread_id
        if stop_reason is not UNSET:
            field_dict["stop_reason"] = stop_reason

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.managed_agents_session_thread_stop_reason import ManagedAgentsSessionThreadStopReason # noqa: PLC0415
        d = dict(src_dict)
        agent_id = d.pop("agent_id")

        created_at = datetime.datetime.fromisoformat(d.pop("created_at"))




        role = d.pop("role")

        root_session_id = d.pop("root_session_id")

        session_id = d.pop("session_id")

        session_path = d.pop("session_path")

        status = d.pop("status")

        thread_id = d.pop("thread_id")

        thread_path = d.pop("thread_path")

        updated_at = datetime.datetime.fromisoformat(d.pop("updated_at"))




        agent_version_id = d.pop("agent_version_id", UNSET)

        _archived_at = d.pop("archived_at", UNSET)
        archived_at: datetime.datetime | Unset
        if isinstance(_archived_at,  Unset):
            archived_at = UNSET
        else:
            archived_at = datetime.datetime.fromisoformat(_archived_at)




        name = d.pop("name", UNSET)

        parent_session_id = d.pop("parent_session_id", UNSET)

        parent_thread_id = d.pop("parent_thread_id", UNSET)

        _stop_reason = d.pop("stop_reason", UNSET)
        stop_reason: ManagedAgentsSessionThreadStopReason | Unset
        if isinstance(_stop_reason,  Unset):
            stop_reason = UNSET
        else:
            stop_reason = ManagedAgentsSessionThreadStopReason.from_dict(_stop_reason)




        managed_agents_session_thread = cls(
            agent_id=agent_id,
            created_at=created_at,
            role=role,
            root_session_id=root_session_id,
            session_id=session_id,
            session_path=session_path,
            status=status,
            thread_id=thread_id,
            thread_path=thread_path,
            updated_at=updated_at,
            agent_version_id=agent_version_id,
            archived_at=archived_at,
            name=name,
            parent_session_id=parent_session_id,
            parent_thread_id=parent_thread_id,
            stop_reason=stop_reason,
        )


        managed_agents_session_thread.additional_properties = d
        return managed_agents_session_thread

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
