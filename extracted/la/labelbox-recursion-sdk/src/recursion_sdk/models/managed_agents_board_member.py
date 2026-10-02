from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="ManagedAgentsBoardMember")



@_attrs_define
class ManagedAgentsBoardMember:
    """ One session on the team as the snapshot saw it: the name it is addressed by, whether it leads, and whether it is
    still live.

        Example:
            {'leader': True, 'name': 'example-name', 'session_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'state':
                'example'}

        Attributes:
            name (str): The name members refer to it by: the thread name for a teammate, the agent's name for the leader.
            session_id (str): The member's session id. Task owners and post authors are recorded by this id.
            leader (bool | Unset): True for the root session, which posts the round and decides.
            state (str | Unset): The member's thread state when the snapshot was read, as list_agents reports it. Omitted
                when the reader did not resolve members.
     """

    name: str
    session_id: str
    leader: bool | Unset = UNSET
    state: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        name = self.name

        session_id = self.session_id

        leader = self.leader

        state = self.state


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "name": name,
            "session_id": session_id,
        })
        if leader is not UNSET:
            field_dict["leader"] = leader
        if state is not UNSET:
            field_dict["state"] = state

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        session_id = d.pop("session_id")

        leader = d.pop("leader", UNSET)

        state = d.pop("state", UNSET)

        managed_agents_board_member = cls(
            name=name,
            session_id=session_id,
            leader=leader,
            state=state,
        )


        managed_agents_board_member.additional_properties = d
        return managed_agents_board_member

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
