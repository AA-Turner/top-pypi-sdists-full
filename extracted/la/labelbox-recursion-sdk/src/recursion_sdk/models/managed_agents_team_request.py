from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.managed_agents_team_request_mode import ManagedAgentsTeamRequestMode
from ..types import UNSET, Unset






T = TypeVar("T", bound="ManagedAgentsTeamRequest")



@_attrs_define
class ManagedAgentsTeamRequest:
    """ Per-session override of the agent's team setting: whether the tree may become a team. Omit the mode to keep the
    agent's setting. The seats a team may fill are the roster's limits.max_concurrent_threads; recruits are sized to the
    claimable work under that cap, and teammates may always message each other directly.

        Example:
            {'mode': 'auto'}

        Attributes:
            mode (ManagedAgentsTeamRequestMode | Unset): auto (default): the board tools are offered and the tree becomes a
                team when the agent posts its first task. on: a team from turn one, briefed as one before it has posted
                anything. off: no board; the agent delegates and waits as a plain coordinator. Omit to keep the agent's setting.
     """

    mode: ManagedAgentsTeamRequestMode | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        mode: str | Unset = UNSET
        if not isinstance(self.mode, Unset):
            mode = self.mode.value



        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if mode is not UNSET:
            field_dict["mode"] = mode

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _mode = d.pop("mode", UNSET)
        mode: ManagedAgentsTeamRequestMode | Unset
        if isinstance(_mode,  Unset):
            mode = UNSET
        else:
            mode = ManagedAgentsTeamRequestMode(_mode)




        managed_agents_team_request = cls(
            mode=mode,
        )


        managed_agents_team_request.additional_properties = d
        return managed_agents_team_request

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
