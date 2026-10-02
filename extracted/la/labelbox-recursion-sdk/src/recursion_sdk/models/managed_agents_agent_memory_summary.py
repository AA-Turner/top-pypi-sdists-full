from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.managed_agents_agent_memory_summary_state import ManagedAgentsAgentMemorySummaryState
from ..types import UNSET, Unset
from typing import cast
import datetime






T = TypeVar("T", bound="ManagedAgentsAgentMemorySummary")



@_attrs_define
class ManagedAgentsAgentMemorySummary:
    """ One agent's living memory collection and automatic learning progress.

        Example:
            {'agent_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'agent_name': 'example', 'effective_model': 'example',
                'failed_session_count': 1, 'last_checked_at': '2026-02-18T09:30:00Z', 'last_updated_at': '2026-02-18T09:30:00Z',
                'memory_count': 1, 'memory_model_ref': 'example', 'memory_store_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d',
                'next_retry_at': '2026-02-18T09:30:00Z', 'pending_session_count': 1, 'revision': 1, 'state': 'waiting',
                'total_bytes': 1}

        Attributes:
            agent_id (str): Agent whose sessions contribute to this memory.
            agent_name (str): Current display name of the agent.
            effective_model (str): Resolved memory model, inherited from this agent unless overridden.
            failed_session_count (int): Sessions whose extraction failed permanently and will not be retried automatically.
            memory_count (int): Number of current memories available for recall.
            pending_session_count (int): Useful session reports waiting to be incorporated.
            revision (int): Committed collection revision, increased by each applied update.
            state (ManagedAgentsAgentMemorySummaryState): Whether memory is waiting for evidence, current, updating, or
                retrying after a failure.
            total_bytes (int): Total bytes of current memory content.
            last_checked_at (datetime.datetime | Unset): Most recent successful automatic memory update, including checks
                that changed nothing.
            last_updated_at (datetime.datetime | Unset): Most recent change to current memory content.
            memory_model_ref (str | Unset): Explicit model override; absent means same as agent.
            memory_store_id (str | Unset): Permanent collection id; absent before its first session starts.
            next_retry_at (datetime.datetime | Unset): Earliest next retry after a failed learning run.
     """

    agent_id: str
    agent_name: str
    effective_model: str
    failed_session_count: int
    memory_count: int
    pending_session_count: int
    revision: int
    state: ManagedAgentsAgentMemorySummaryState
    total_bytes: int
    last_checked_at: datetime.datetime | Unset = UNSET
    last_updated_at: datetime.datetime | Unset = UNSET
    memory_model_ref: str | Unset = UNSET
    memory_store_id: str | Unset = UNSET
    next_retry_at: datetime.datetime | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        agent_id = self.agent_id

        agent_name = self.agent_name

        effective_model = self.effective_model

        failed_session_count = self.failed_session_count

        memory_count = self.memory_count

        pending_session_count = self.pending_session_count

        revision = self.revision

        state = self.state.value

        total_bytes = self.total_bytes

        last_checked_at: str | Unset = UNSET
        if not isinstance(self.last_checked_at, Unset):
            last_checked_at = self.last_checked_at.isoformat()

        last_updated_at: str | Unset = UNSET
        if not isinstance(self.last_updated_at, Unset):
            last_updated_at = self.last_updated_at.isoformat()

        memory_model_ref = self.memory_model_ref

        memory_store_id = self.memory_store_id

        next_retry_at: str | Unset = UNSET
        if not isinstance(self.next_retry_at, Unset):
            next_retry_at = self.next_retry_at.isoformat()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "agent_id": agent_id,
            "agent_name": agent_name,
            "effective_model": effective_model,
            "failed_session_count": failed_session_count,
            "memory_count": memory_count,
            "pending_session_count": pending_session_count,
            "revision": revision,
            "state": state,
            "total_bytes": total_bytes,
        })
        if last_checked_at is not UNSET:
            field_dict["last_checked_at"] = last_checked_at
        if last_updated_at is not UNSET:
            field_dict["last_updated_at"] = last_updated_at
        if memory_model_ref is not UNSET:
            field_dict["memory_model_ref"] = memory_model_ref
        if memory_store_id is not UNSET:
            field_dict["memory_store_id"] = memory_store_id
        if next_retry_at is not UNSET:
            field_dict["next_retry_at"] = next_retry_at

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        agent_id = d.pop("agent_id")

        agent_name = d.pop("agent_name")

        effective_model = d.pop("effective_model")

        failed_session_count = d.pop("failed_session_count")

        memory_count = d.pop("memory_count")

        pending_session_count = d.pop("pending_session_count")

        revision = d.pop("revision")

        state = ManagedAgentsAgentMemorySummaryState(d.pop("state"))




        total_bytes = d.pop("total_bytes")

        _last_checked_at = d.pop("last_checked_at", UNSET)
        last_checked_at: datetime.datetime | Unset
        if isinstance(_last_checked_at,  Unset):
            last_checked_at = UNSET
        else:
            last_checked_at = datetime.datetime.fromisoformat(_last_checked_at)




        _last_updated_at = d.pop("last_updated_at", UNSET)
        last_updated_at: datetime.datetime | Unset
        if isinstance(_last_updated_at,  Unset):
            last_updated_at = UNSET
        else:
            last_updated_at = datetime.datetime.fromisoformat(_last_updated_at)




        memory_model_ref = d.pop("memory_model_ref", UNSET)

        memory_store_id = d.pop("memory_store_id", UNSET)

        _next_retry_at = d.pop("next_retry_at", UNSET)
        next_retry_at: datetime.datetime | Unset
        if isinstance(_next_retry_at,  Unset):
            next_retry_at = UNSET
        else:
            next_retry_at = datetime.datetime.fromisoformat(_next_retry_at)




        managed_agents_agent_memory_summary = cls(
            agent_id=agent_id,
            agent_name=agent_name,
            effective_model=effective_model,
            failed_session_count=failed_session_count,
            memory_count=memory_count,
            pending_session_count=pending_session_count,
            revision=revision,
            state=state,
            total_bytes=total_bytes,
            last_checked_at=last_checked_at,
            last_updated_at=last_updated_at,
            memory_model_ref=memory_model_ref,
            memory_store_id=memory_store_id,
            next_retry_at=next_retry_at,
        )


        managed_agents_agent_memory_summary.additional_properties = d
        return managed_agents_agent_memory_summary

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
