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
  from ..models.managed_agents_gestalt_session_row import ManagedAgentsGestaltSessionRow





T = TypeVar("T", bound="ManagedAgentsSessionGestaltChange")



@_attrs_define
class ManagedAgentsSessionGestaltChange:
    """ One Server-Sent Event of streamSessionGestalt: the root sessions whose rows changed since the previous frame, with
    the read timestamp to resume from.

        Example:
            {'as_of': '2026-02-18T09:30:00Z', 'reset': True, 'sessions': [{'agent_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'created_at': '2026-02-18T09:30:00Z', 'deleted': True,
                'execution_state': 'provisioning', 'failed': True, 'last_activity_at': '2026-02-18T09:30:00Z', 'session_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'status': 'active', 'updated_at': '2026-02-18T09:30:00Z'}]}

        Attributes:
            as_of (datetime.datetime): Read timestamp of this frame; also sent as the SSE id, so a reconnect with Last-
                Event-ID resumes here.
            sessions (list[ManagedAgentsGestaltSessionRow] | None): Roots in the window whose row changed since the previous
                frame, each carrying its whole current state; merge them by session_id. A row with deleted true has been
                removed.
            reset (bool | Unset): True when more changed than one frame carries. Discard the gestalt and take a fresh
                snapshot; sessions is empty.
     """

    as_of: datetime.datetime
    sessions: list[ManagedAgentsGestaltSessionRow] | None
    reset: bool | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.managed_agents_gestalt_session_row import ManagedAgentsGestaltSessionRow # noqa: PLC0415
        as_of = self.as_of.isoformat()

        sessions: list[dict[str, Any]] | None
        if isinstance(self.sessions, list):
            sessions = []
            for sessions_type_0_item_data in self.sessions:
                sessions_type_0_item = sessions_type_0_item_data.to_dict()
                sessions.append(sessions_type_0_item)


        else:
            sessions = self.sessions

        reset = self.reset


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "as_of": as_of,
            "sessions": sessions,
        })
        if reset is not UNSET:
            field_dict["reset"] = reset

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.managed_agents_gestalt_session_row import ManagedAgentsGestaltSessionRow # noqa: PLC0415
        d = dict(src_dict)
        as_of = datetime.datetime.fromisoformat(d.pop("as_of"))




        def _parse_sessions(data: object) -> list[ManagedAgentsGestaltSessionRow] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                sessions_type_0 = []
                _sessions_type_0 = data
                for sessions_type_0_item_data in (_sessions_type_0):
                    sessions_type_0_item = ManagedAgentsGestaltSessionRow.from_dict(sessions_type_0_item_data)



                    sessions_type_0.append(sessions_type_0_item)

                return sessions_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[ManagedAgentsGestaltSessionRow] | None, data)

        sessions = _parse_sessions(d.pop("sessions"))


        reset = d.pop("reset", UNSET)

        managed_agents_session_gestalt_change = cls(
            as_of=as_of,
            sessions=sessions,
            reset=reset,
        )


        managed_agents_session_gestalt_change.additional_properties = d
        return managed_agents_session_gestalt_change

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
