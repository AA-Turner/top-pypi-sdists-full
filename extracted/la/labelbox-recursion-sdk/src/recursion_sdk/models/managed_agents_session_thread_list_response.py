from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.managed_agents_session_thread import ManagedAgentsSessionThread





T = TypeVar("T", bound="ManagedAgentsSessionThreadListResponse")



@_attrs_define
class ManagedAgentsSessionThreadListResponse:
    """ Response body of GET /v1/sessions/{session_id}/threads. The path id may name any session in a multi-agent tree; the
    registry returned is always the whole tree's, resolved through that session's root, so a subagent id and its root id
    return the same set.

        Example:
            {'threads': [{'agent_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'agent_version_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'archived_at': '2026-02-18T09:30:00Z', 'created_at':
                '2026-02-18T09:30:00Z', 'name': 'example-name', 'parent_session_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d',
                'parent_thread_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'role': 'user', 'root_session_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'session_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'session_path':
                'example', 'status': 'example', 'stop_reason': {'key': 'example'}, 'thread_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'thread_path': 'example', 'updated_at': '2026-02-18T09:30:00Z'}]}

        Attributes:
            threads (list[ManagedAgentsSessionThread] | None): Threads belonging to the session tree the path session is
                part of. May be null or an empty array; both mean the tree has no registered threads. Threads on sessions the
                caller may not read are dropped.
     """

    threads: list[ManagedAgentsSessionThread] | None
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.managed_agents_session_thread import ManagedAgentsSessionThread # noqa: PLC0415
        threads: list[dict[str, Any]] | None
        if isinstance(self.threads, list):
            threads = []
            for threads_type_0_item_data in self.threads:
                threads_type_0_item = threads_type_0_item_data.to_dict()
                threads.append(threads_type_0_item)


        else:
            threads = self.threads


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "threads": threads,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.managed_agents_session_thread import ManagedAgentsSessionThread # noqa: PLC0415
        d = dict(src_dict)
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


        managed_agents_session_thread_list_response = cls(
            threads=threads,
        )


        managed_agents_session_thread_list_response.additional_properties = d
        return managed_agents_session_thread_list_response

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
