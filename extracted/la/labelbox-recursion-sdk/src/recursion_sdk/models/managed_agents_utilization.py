from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.managed_agents_utilization_basis import ManagedAgentsUtilizationBasis
from ..models.managed_agents_utilization_workload import ManagedAgentsUtilizationWorkload
from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.managed_agents_band import ManagedAgentsBand





T = TypeVar("T", bound="ManagedAgentsUtilization")



@_attrs_define
class ManagedAgentsUtilization:
    """ How much of a session hour the agent spends generating.

        Example:
            {'basis': 'agent_history', 'sessionHours': {'high': 1.5, 'low': 1.5, 'typical': 1.5}, 'sessions': 1, 'share':
                {'high': 1.5, 'low': 1.5, 'typical': 1.5}, 'workload': 'interactive'}

        Attributes:
            basis (ManagedAgentsUtilizationBasis): Whether the share comes from this agent's own completed sessions or from
                the workload prior.
            session_hours (ManagedAgentsBand): Low, typical and high values: the 25th, 50th and 75th percentiles. Example:
                {'high': 1.5, 'low': 1.5, 'typical': 1.5}.
            sessions (int): Completed sessions behind agent_history; zero otherwise.
            share (ManagedAgentsBand): Low, typical and high values: the 25th, 50th and 75th percentiles. Example: {'high':
                1.5, 'low': 1.5, 'typical': 1.5}.
            workload (ManagedAgentsUtilizationWorkload | Unset): Workload prior used when basis is workload_prior.
     """

    basis: ManagedAgentsUtilizationBasis
    session_hours: ManagedAgentsBand
    sessions: int
    share: ManagedAgentsBand
    workload: ManagedAgentsUtilizationWorkload | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.managed_agents_band import ManagedAgentsBand # noqa: PLC0415
        basis = self.basis.value

        session_hours = self.session_hours.to_dict()

        sessions = self.sessions

        share = self.share.to_dict()

        workload: str | Unset = UNSET
        if not isinstance(self.workload, Unset):
            workload = self.workload.value



        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "basis": basis,
            "sessionHours": session_hours,
            "sessions": sessions,
            "share": share,
        })
        if workload is not UNSET:
            field_dict["workload"] = workload

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.managed_agents_band import ManagedAgentsBand # noqa: PLC0415
        d = dict(src_dict)
        basis = ManagedAgentsUtilizationBasis(d.pop("basis"))




        session_hours = ManagedAgentsBand.from_dict(d.pop("sessionHours"))




        sessions = d.pop("sessions")

        share = ManagedAgentsBand.from_dict(d.pop("share"))




        _workload = d.pop("workload", UNSET)
        workload: ManagedAgentsUtilizationWorkload | Unset
        if isinstance(_workload,  Unset):
            workload = UNSET
        else:
            workload = ManagedAgentsUtilizationWorkload(_workload)




        managed_agents_utilization = cls(
            basis=basis,
            session_hours=session_hours,
            sessions=sessions,
            share=share,
            workload=workload,
        )


        managed_agents_utilization.additional_properties = d
        return managed_agents_utilization

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
