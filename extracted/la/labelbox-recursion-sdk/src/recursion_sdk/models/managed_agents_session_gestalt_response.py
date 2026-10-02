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





T = TypeVar("T", bound="ManagedAgentsSessionGestaltResponse")



@_attrs_define
class ManagedAgentsSessionGestaltResponse:
    """ Response body of GET /v1/sessions/gestalt: a compact snapshot of every root session an organization created in a
    window, read at one instant. Designed to be drawn whole -- one tile per session -- and kept current by
    streamSessionGestalt rather than re-read.

        Example:
            {'as_of': '2026-02-18T09:30:00Z', 'sessions': [{'agent_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d',
                'created_at': '2026-02-18T09:30:00Z', 'deleted': True, 'execution_state': 'provisioning', 'failed': True,
                'last_activity_at': '2026-02-18T09:30:00Z', 'session_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'status':
                'active', 'updated_at': '2026-02-18T09:30:00Z'}], 'truncated': True}

        Attributes:
            as_of (datetime.datetime): Read timestamp of this snapshot. Pass it as after to streamSessionGestalt to receive
                every change since.
            sessions (list[ManagedAgentsGestaltSessionRow] | None): Every live root session created at or after since that
                the caller may see, newest first. Rows the caller's access policy does not permit are omitted silently.
            truncated (bool | Unset): True when the window held more than 5000 root sessions and only the newest 5000 are
                listed.
     """

    as_of: datetime.datetime
    sessions: list[ManagedAgentsGestaltSessionRow] | None
    truncated: bool | Unset = UNSET
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

        truncated = self.truncated


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "as_of": as_of,
            "sessions": sessions,
        })
        if truncated is not UNSET:
            field_dict["truncated"] = truncated

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


        truncated = d.pop("truncated", UNSET)

        managed_agents_session_gestalt_response = cls(
            as_of=as_of,
            sessions=sessions,
            truncated=truncated,
        )


        managed_agents_session_gestalt_response.additional_properties = d
        return managed_agents_session_gestalt_response

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
