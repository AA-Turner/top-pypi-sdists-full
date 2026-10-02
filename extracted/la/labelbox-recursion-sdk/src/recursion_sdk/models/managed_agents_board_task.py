from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.managed_agents_board_task_kind import ManagedAgentsBoardTaskKind
from ..models.managed_agents_board_task_status import ManagedAgentsBoardTaskStatus
from ..types import UNSET, Unset
from typing import cast
import datetime

if TYPE_CHECKING:
  from ..models.managed_agents_board_note import ManagedAgentsBoardNote
  from ..models.managed_agents_board_outcome import ManagedAgentsBoardOutcome





T = TypeVar("T", bound="ManagedAgentsBoardTask")



@_attrs_define
class ManagedAgentsBoardTask:
    """ One row of a team's shared task board: a unit of work a member claims, does, and marks done, with its brief,
    dependencies, owner, outcome, and notes.

        Example:
            {'artifacts': ['example'], 'blocked_on': ['example'], 'body': 'example', 'claim_generation': 1, 'created_at':
                '2026-02-18T09:30:00Z', 'created_by': 'example', 'kind': 'task', 'notes': [{'at': '2026-02-18T09:30:00Z', 'by':
                'example', 'text': 'example'}], 'outcome': {'artifacts': ['example'], 'confidence': 'example', 'summary':
                'example'}, 'owner_session_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'seq': 1, 'status': 'open', 'task_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'title': 'example', 'updated_at': '2026-02-18T09:30:00Z'}

        Attributes:
            body (str): The self-contained brief the owner works from: what to produce, where to write it, what a good
                result contains, and any shared convention the round must follow.
            claim_generation (int): Incremented on every claim so a stale owner cannot update a task that was released and
                re-claimed.
            created_at (datetime.datetime): When the task was posted.
            created_by (str): Session id of the member who posted the task.
            kind (ManagedAgentsBoardTaskKind): task: work with a named output. explore: one angle on an open question, whose
                proposal a review reads. review: read another member's output or proposal and leave a verdict as a note.
            seq (int): Tree-local ordinal, assigned in posting order. Members and the console address the task by its label,
                "T" followed by this number.
            status (ManagedAgentsBoardTaskStatus): open: claimable. claimed: owned and in progress. blocked: waiting on the
                tasks in blocked_on, or on something the owner named in a note. done: finished, with an outcome. dropped:
                withdrawn by the leader.
            task_id (str): Server-assigned id of the task, stable across status changes.
            title (str): One-line title shown on the board and in the console.
            updated_at (datetime.datetime): When the task last changed status, owner, outcome, or notes.
            artifacts (list[str] | Unset): Sandbox paths the task is expected to write, named by the poster so every member
                sees which paths belong to whom.
            blocked_on (list[str] | Unset): Task ids this task waits on. The task becomes claimable once every one of them
                is done.
            notes (list[ManagedAgentsBoardNote] | Unset): Notes attached to the task in the order they were added.
            outcome (ManagedAgentsBoardOutcome | Unset): What a done task produced: the owner's summary, its confidence, and
                the artifact paths a reader or reviewer can open. Example: {'artifacts': ['example'], 'confidence': 'example',
                'summary': 'example'}.
            owner_session_id (str | Unset): Session id of the member holding the claim. Empty while the task is open or
                after a claim was released.
     """

    body: str
    claim_generation: int
    created_at: datetime.datetime
    created_by: str
    kind: ManagedAgentsBoardTaskKind
    seq: int
    status: ManagedAgentsBoardTaskStatus
    task_id: str
    title: str
    updated_at: datetime.datetime
    artifacts: list[str] | Unset = UNSET
    blocked_on: list[str] | Unset = UNSET
    notes: list[ManagedAgentsBoardNote] | Unset = UNSET
    outcome: ManagedAgentsBoardOutcome | Unset = UNSET
    owner_session_id: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.managed_agents_board_note import ManagedAgentsBoardNote # noqa: PLC0415
        from ..models.managed_agents_board_outcome import ManagedAgentsBoardOutcome # noqa: PLC0415
        body = self.body

        claim_generation = self.claim_generation

        created_at = self.created_at.isoformat()

        created_by = self.created_by

        kind = self.kind.value

        seq = self.seq

        status = self.status.value

        task_id = self.task_id

        title = self.title

        updated_at = self.updated_at.isoformat()

        artifacts: list[str] | Unset = UNSET
        if not isinstance(self.artifacts, Unset):
            artifacts = self.artifacts



        blocked_on: list[str] | Unset = UNSET
        if not isinstance(self.blocked_on, Unset):
            blocked_on = self.blocked_on



        notes: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.notes, Unset):
            notes = []
            for notes_item_data in self.notes:
                notes_item = notes_item_data.to_dict()
                notes.append(notes_item)



        outcome: dict[str, Any] | Unset = UNSET
        if not isinstance(self.outcome, Unset):
            outcome = self.outcome.to_dict()

        owner_session_id = self.owner_session_id


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "body": body,
            "claim_generation": claim_generation,
            "created_at": created_at,
            "created_by": created_by,
            "kind": kind,
            "seq": seq,
            "status": status,
            "task_id": task_id,
            "title": title,
            "updated_at": updated_at,
        })
        if artifacts is not UNSET:
            field_dict["artifacts"] = artifacts
        if blocked_on is not UNSET:
            field_dict["blocked_on"] = blocked_on
        if notes is not UNSET:
            field_dict["notes"] = notes
        if outcome is not UNSET:
            field_dict["outcome"] = outcome
        if owner_session_id is not UNSET:
            field_dict["owner_session_id"] = owner_session_id

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.managed_agents_board_note import ManagedAgentsBoardNote # noqa: PLC0415
        from ..models.managed_agents_board_outcome import ManagedAgentsBoardOutcome # noqa: PLC0415
        d = dict(src_dict)
        body = d.pop("body")

        claim_generation = d.pop("claim_generation")

        created_at = datetime.datetime.fromisoformat(d.pop("created_at"))




        created_by = d.pop("created_by")

        kind = ManagedAgentsBoardTaskKind(d.pop("kind"))




        seq = d.pop("seq")

        status = ManagedAgentsBoardTaskStatus(d.pop("status"))




        task_id = d.pop("task_id")

        title = d.pop("title")

        updated_at = datetime.datetime.fromisoformat(d.pop("updated_at"))




        artifacts = cast(list[str], d.pop("artifacts", UNSET))


        blocked_on = cast(list[str], d.pop("blocked_on", UNSET))


        _notes = d.pop("notes", UNSET)
        notes: list[ManagedAgentsBoardNote] | Unset = UNSET
        if _notes is not UNSET:
            notes = []
            for notes_item_data in _notes:
                notes_item = ManagedAgentsBoardNote.from_dict(notes_item_data)



                notes.append(notes_item)


        _outcome = d.pop("outcome", UNSET)
        outcome: ManagedAgentsBoardOutcome | Unset
        if isinstance(_outcome,  Unset):
            outcome = UNSET
        else:
            outcome = ManagedAgentsBoardOutcome.from_dict(_outcome)




        owner_session_id = d.pop("owner_session_id", UNSET)

        managed_agents_board_task = cls(
            body=body,
            claim_generation=claim_generation,
            created_at=created_at,
            created_by=created_by,
            kind=kind,
            seq=seq,
            status=status,
            task_id=task_id,
            title=title,
            updated_at=updated_at,
            artifacts=artifacts,
            blocked_on=blocked_on,
            notes=notes,
            outcome=outcome,
            owner_session_id=owner_session_id,
        )


        managed_agents_board_task.additional_properties = d
        return managed_agents_board_task

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
