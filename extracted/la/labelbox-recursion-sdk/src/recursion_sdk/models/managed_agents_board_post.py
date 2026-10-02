from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.managed_agents_board_post_kind import ManagedAgentsBoardPostKind
from ..types import UNSET, Unset
from typing import cast
import datetime






T = TypeVar("T", bound="ManagedAgentsBoardPost")



@_attrs_define
class ManagedAgentsBoardPost:
    """ A tree-wide post on the board: a pinned notice, a teammate's recommendation, or the leader's decision that closes an
    exploratory round.

        Example:
            {'created_at': '2026-02-18T09:30:00Z', 'created_by': 'example', 'kind': 'notice', 'post_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'task_ids': ['example'], 'text': 'example'}

        Attributes:
            created_at (datetime.datetime): When the post was made.
            created_by (str): Session id of the member who posted it.
            kind (ManagedAgentsBoardPostKind): notice: a fact every member needs, pinned into each member's briefing.
                recommendation: a teammate's pick among a round's proposals with its rationale. decision: the leader's call on
                which proposals carry forward; at most one per board.
            post_id (str): Server-assigned id of the post.
            text (str): The post's text: the notice, or the rationale behind a recommendation or decision.
            task_ids (list[str] | Unset): Tasks the post refers to. A decision names the winning proposals; a recommendation
                names the teammate's pick.
     """

    created_at: datetime.datetime
    created_by: str
    kind: ManagedAgentsBoardPostKind
    post_id: str
    text: str
    task_ids: list[str] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        created_at = self.created_at.isoformat()

        created_by = self.created_by

        kind = self.kind.value

        post_id = self.post_id

        text = self.text

        task_ids: list[str] | Unset = UNSET
        if not isinstance(self.task_ids, Unset):
            task_ids = self.task_ids




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "created_at": created_at,
            "created_by": created_by,
            "kind": kind,
            "post_id": post_id,
            "text": text,
        })
        if task_ids is not UNSET:
            field_dict["task_ids"] = task_ids

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        created_at = datetime.datetime.fromisoformat(d.pop("created_at"))




        created_by = d.pop("created_by")

        kind = ManagedAgentsBoardPostKind(d.pop("kind"))




        post_id = d.pop("post_id")

        text = d.pop("text")

        task_ids = cast(list[str], d.pop("task_ids", UNSET))


        managed_agents_board_post = cls(
            created_at=created_at,
            created_by=created_by,
            kind=kind,
            post_id=post_id,
            text=text,
            task_ids=task_ids,
        )


        managed_agents_board_post.additional_properties = d
        return managed_agents_board_post

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
