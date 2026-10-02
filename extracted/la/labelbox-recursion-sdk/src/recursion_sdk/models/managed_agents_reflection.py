from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.managed_agents_reflection_status import ManagedAgentsReflectionStatus
from ..models.managed_agents_reflection_triggered_by import ManagedAgentsReflectionTriggeredBy
from ..types import UNSET, Unset
from typing import cast
import datetime






T = TypeVar("T", bound="ManagedAgentsReflection")



@_attrs_define
class ManagedAgentsReflection:
    """ One memory consolidation: session reports in, atomic changes to its living memory collection out. It runs as an
    ordinary observable session, so the whole run is inspectable through driver_session_id.

        Example:
            {'added_count': 1, 'agent_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'agent_version_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'base_revision': 1, 'created_at': '2026-02-18T09:30:00Z',
                'digest_count': 1, 'driver_session_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'ended_at':
                '2026-02-18T09:30:00Z', 'error_message': 'example', 'error_type': 'example', 'input_session_ids': ['example'],
                'instructions': 'example', 'memory_store_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'merged_count': 1,
                'model': 'example', 'model_ref_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'organization_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'reflection_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d',
                'retired_count': 1, 'status': 'pending', 'trigger_window': 'example', 'triggered_by': 'schedule', 'updated_at':
                '2026-02-18T09:30:00Z', 'updated_count': 1}

        Attributes:
            added_count (int): Memories added by this run.
            agent_id (str): Agent whose memory this run curates.
            base_revision (int): Collection revision read by this run.
            created_at (datetime.datetime): Server-assigned RFC 3339 timestamp of when the run was created.
            memory_store_id (str): Stable memory collection updated by this run.
            merged_count (int): Memories merged into another memory.
            organization_id (str): Organization that owns this record.
            reflection_id (str): Server-assigned id of the run.
            retired_count (int): Memories retired without a replacement.
            status (ManagedAgentsReflectionStatus): Where the run is.
            triggered_by (ManagedAgentsReflectionTriggeredBy): What started the run: a schedule tick, the digest counter
                crossing its threshold, or an operator.
            updated_at (datetime.datetime): Server-assigned RFC 3339 timestamp of the most recent change.
            updated_count (int): Existing memories refined by this run.
            agent_version_id (str | Unset): Version of the agent under study when the run started.
            digest_count (int | Unset): Number of digests read.
            driver_session_id (str | Unset): The observable session running this consolidation. Stream it to watch the run.
            ended_at (datetime.datetime | Unset): Set when the run reached a terminal status.
            error_message (str | Unset): Human-readable failure detail.
            error_type (str | Unset): Classification of a failure.
            input_session_ids (list[str] | Unset): Sessions whose digests this run read.
            instructions (str | Unset): Operator guidance steering what to synthesize. Capped at 4096 characters.
            model (str | Unset): Gateway or provider model string that ran the consolidation. Empty when model_ref_id names
                a registered reference instead.
            model_ref_id (str | Unset): Canonical model-reference UUID that ran the consolidation. Empty when model names a
                gateway model instead.
            trigger_window (str | Unset): Deterministic identifier of the trigger occasion. Unique per agent, so a duplicate
                scan cannot start the run twice.
     """

    added_count: int
    agent_id: str
    base_revision: int
    created_at: datetime.datetime
    memory_store_id: str
    merged_count: int
    organization_id: str
    reflection_id: str
    retired_count: int
    status: ManagedAgentsReflectionStatus
    triggered_by: ManagedAgentsReflectionTriggeredBy
    updated_at: datetime.datetime
    updated_count: int
    agent_version_id: str | Unset = UNSET
    digest_count: int | Unset = UNSET
    driver_session_id: str | Unset = UNSET
    ended_at: datetime.datetime | Unset = UNSET
    error_message: str | Unset = UNSET
    error_type: str | Unset = UNSET
    input_session_ids: list[str] | Unset = UNSET
    instructions: str | Unset = UNSET
    model: str | Unset = UNSET
    model_ref_id: str | Unset = UNSET
    trigger_window: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        added_count = self.added_count

        agent_id = self.agent_id

        base_revision = self.base_revision

        created_at = self.created_at.isoformat()

        memory_store_id = self.memory_store_id

        merged_count = self.merged_count

        organization_id = self.organization_id

        reflection_id = self.reflection_id

        retired_count = self.retired_count

        status = self.status.value

        triggered_by = self.triggered_by.value

        updated_at = self.updated_at.isoformat()

        updated_count = self.updated_count

        agent_version_id = self.agent_version_id

        digest_count = self.digest_count

        driver_session_id = self.driver_session_id

        ended_at: str | Unset = UNSET
        if not isinstance(self.ended_at, Unset):
            ended_at = self.ended_at.isoformat()

        error_message = self.error_message

        error_type = self.error_type

        input_session_ids: list[str] | Unset = UNSET
        if not isinstance(self.input_session_ids, Unset):
            input_session_ids = self.input_session_ids



        instructions = self.instructions

        model = self.model

        model_ref_id = self.model_ref_id

        trigger_window = self.trigger_window


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "added_count": added_count,
            "agent_id": agent_id,
            "base_revision": base_revision,
            "created_at": created_at,
            "memory_store_id": memory_store_id,
            "merged_count": merged_count,
            "organization_id": organization_id,
            "reflection_id": reflection_id,
            "retired_count": retired_count,
            "status": status,
            "triggered_by": triggered_by,
            "updated_at": updated_at,
            "updated_count": updated_count,
        })
        if agent_version_id is not UNSET:
            field_dict["agent_version_id"] = agent_version_id
        if digest_count is not UNSET:
            field_dict["digest_count"] = digest_count
        if driver_session_id is not UNSET:
            field_dict["driver_session_id"] = driver_session_id
        if ended_at is not UNSET:
            field_dict["ended_at"] = ended_at
        if error_message is not UNSET:
            field_dict["error_message"] = error_message
        if error_type is not UNSET:
            field_dict["error_type"] = error_type
        if input_session_ids is not UNSET:
            field_dict["input_session_ids"] = input_session_ids
        if instructions is not UNSET:
            field_dict["instructions"] = instructions
        if model is not UNSET:
            field_dict["model"] = model
        if model_ref_id is not UNSET:
            field_dict["model_ref_id"] = model_ref_id
        if trigger_window is not UNSET:
            field_dict["trigger_window"] = trigger_window

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        added_count = d.pop("added_count")

        agent_id = d.pop("agent_id")

        base_revision = d.pop("base_revision")

        created_at = datetime.datetime.fromisoformat(d.pop("created_at"))




        memory_store_id = d.pop("memory_store_id")

        merged_count = d.pop("merged_count")

        organization_id = d.pop("organization_id")

        reflection_id = d.pop("reflection_id")

        retired_count = d.pop("retired_count")

        status = ManagedAgentsReflectionStatus(d.pop("status"))




        triggered_by = ManagedAgentsReflectionTriggeredBy(d.pop("triggered_by"))




        updated_at = datetime.datetime.fromisoformat(d.pop("updated_at"))




        updated_count = d.pop("updated_count")

        agent_version_id = d.pop("agent_version_id", UNSET)

        digest_count = d.pop("digest_count", UNSET)

        driver_session_id = d.pop("driver_session_id", UNSET)

        _ended_at = d.pop("ended_at", UNSET)
        ended_at: datetime.datetime | Unset
        if isinstance(_ended_at,  Unset):
            ended_at = UNSET
        else:
            ended_at = datetime.datetime.fromisoformat(_ended_at)




        error_message = d.pop("error_message", UNSET)

        error_type = d.pop("error_type", UNSET)

        input_session_ids = cast(list[str], d.pop("input_session_ids", UNSET))


        instructions = d.pop("instructions", UNSET)

        model = d.pop("model", UNSET)

        model_ref_id = d.pop("model_ref_id", UNSET)

        trigger_window = d.pop("trigger_window", UNSET)

        managed_agents_reflection = cls(
            added_count=added_count,
            agent_id=agent_id,
            base_revision=base_revision,
            created_at=created_at,
            memory_store_id=memory_store_id,
            merged_count=merged_count,
            organization_id=organization_id,
            reflection_id=reflection_id,
            retired_count=retired_count,
            status=status,
            triggered_by=triggered_by,
            updated_at=updated_at,
            updated_count=updated_count,
            agent_version_id=agent_version_id,
            digest_count=digest_count,
            driver_session_id=driver_session_id,
            ended_at=ended_at,
            error_message=error_message,
            error_type=error_type,
            input_session_ids=input_session_ids,
            instructions=instructions,
            model=model,
            model_ref_id=model_ref_id,
            trigger_window=trigger_window,
        )


        managed_agents_reflection.additional_properties = d
        return managed_agents_reflection

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
