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
  from ..models.managed_agents_board_member import ManagedAgentsBoardMember
  from ..models.managed_agents_board_post import ManagedAgentsBoardPost
  from ..models.managed_agents_board_task import ManagedAgentsBoardTask





T = TypeVar("T", bound="ManagedAgentsBoard")



@_attrs_define
class ManagedAgentsBoard:
    """ A snapshot of one session tree's shared task board: its tasks, posts, and members. Present once the tree has entered
    team state; an auto-mode tree that has not posted reads as an empty board.

        Example:
            {'as_of': '2026-02-18T09:30:00Z', 'members': [{'leader': True, 'name': 'example-name', 'session_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'state': 'example'}], 'posts': [{'created_at': '2026-02-18T09:30:00Z',
                'created_by': 'example', 'kind': 'notice', 'post_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'task_ids':
                ['example'], 'text': 'example'}], 'tasks': [{'artifacts': ['example'], 'blocked_on': ['example'], 'body':
                'example', 'claim_generation': 1, 'created_at': '2026-02-18T09:30:00Z', 'created_by': 'example', 'kind': 'task',
                'notes': [{'at': '2026-02-18T09:30:00Z', 'by': 'example', 'text': 'example'}], 'outcome': {'artifacts':
                ['example'], 'confidence': 'example', 'summary': 'example'}, 'owner_session_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'seq': 1, 'status': 'open', 'task_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'title': 'example', 'updated_at': '2026-02-18T09:30:00Z'}]}

        Attributes:
            as_of (datetime.datetime): RFC 3339 server time at which the snapshot was read, so a reader can age claims.
            posts (list[ManagedAgentsBoardPost] | None): Every notice, recommendation, and decision in posting order.
            tasks (list[ManagedAgentsBoardTask] | None): Every task on the board in posting order, including done and
                dropped ones.
            members (list[ManagedAgentsBoardMember] | Unset): The sessions that may act on the board. Omitted when the
                reader did not resolve members.
     """

    as_of: datetime.datetime
    posts: list[ManagedAgentsBoardPost] | None
    tasks: list[ManagedAgentsBoardTask] | None
    members: list[ManagedAgentsBoardMember] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.managed_agents_board_member import ManagedAgentsBoardMember # noqa: PLC0415
        from ..models.managed_agents_board_post import ManagedAgentsBoardPost # noqa: PLC0415
        from ..models.managed_agents_board_task import ManagedAgentsBoardTask # noqa: PLC0415
        as_of = self.as_of.isoformat()

        posts: list[dict[str, Any]] | None
        if isinstance(self.posts, list):
            posts = []
            for posts_type_0_item_data in self.posts:
                posts_type_0_item = posts_type_0_item_data.to_dict()
                posts.append(posts_type_0_item)


        else:
            posts = self.posts

        tasks: list[dict[str, Any]] | None
        if isinstance(self.tasks, list):
            tasks = []
            for tasks_type_0_item_data in self.tasks:
                tasks_type_0_item = tasks_type_0_item_data.to_dict()
                tasks.append(tasks_type_0_item)


        else:
            tasks = self.tasks

        members: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.members, Unset):
            members = []
            for members_item_data in self.members:
                members_item = members_item_data.to_dict()
                members.append(members_item)




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "as_of": as_of,
            "posts": posts,
            "tasks": tasks,
        })
        if members is not UNSET:
            field_dict["members"] = members

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.managed_agents_board_member import ManagedAgentsBoardMember # noqa: PLC0415
        from ..models.managed_agents_board_post import ManagedAgentsBoardPost # noqa: PLC0415
        from ..models.managed_agents_board_task import ManagedAgentsBoardTask # noqa: PLC0415
        d = dict(src_dict)
        as_of = datetime.datetime.fromisoformat(d.pop("as_of"))




        def _parse_posts(data: object) -> list[ManagedAgentsBoardPost] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                posts_type_0 = []
                _posts_type_0 = data
                for posts_type_0_item_data in (_posts_type_0):
                    posts_type_0_item = ManagedAgentsBoardPost.from_dict(posts_type_0_item_data)



                    posts_type_0.append(posts_type_0_item)

                return posts_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[ManagedAgentsBoardPost] | None, data)

        posts = _parse_posts(d.pop("posts"))


        def _parse_tasks(data: object) -> list[ManagedAgentsBoardTask] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                tasks_type_0 = []
                _tasks_type_0 = data
                for tasks_type_0_item_data in (_tasks_type_0):
                    tasks_type_0_item = ManagedAgentsBoardTask.from_dict(tasks_type_0_item_data)



                    tasks_type_0.append(tasks_type_0_item)

                return tasks_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[ManagedAgentsBoardTask] | None, data)

        tasks = _parse_tasks(d.pop("tasks"))


        _members = d.pop("members", UNSET)
        members: list[ManagedAgentsBoardMember] | Unset = UNSET
        if _members is not UNSET:
            members = []
            for members_item_data in _members:
                members_item = ManagedAgentsBoardMember.from_dict(members_item_data)



                members.append(members_item)


        managed_agents_board = cls(
            as_of=as_of,
            posts=posts,
            tasks=tasks,
            members=members,
        )


        managed_agents_board.additional_properties = d
        return managed_agents_board

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
