from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="ManagedAgentsIntegrationConnectionUsage")



@_attrs_define
class ManagedAgentsIntegrationConnectionUsage:
    """ Current agent and pinned automation runtime usage of a connection.

        Example:
            {'agents': 1, 'automations': 1}

        Attributes:
            agents (int): Distinct agents whose current version selects this connection.
            automations (int): Distinct canonical automations, including paused ones, whose pinned agent version selects
                this connection.
     """

    agents: int
    automations: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        agents = self.agents

        automations = self.automations


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "agents": agents,
            "automations": automations,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        agents = d.pop("agents")

        automations = d.pop("automations")

        managed_agents_integration_connection_usage = cls(
            agents=agents,
            automations=automations,
        )


        managed_agents_integration_connection_usage.additional_properties = d
        return managed_agents_integration_connection_usage

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
