from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="ManagedAgentsEnvironmentNetworkPolicy")



@_attrs_define
class ManagedAgentsEnvironmentNetworkPolicy:
    """ Runs egress rules. On update, omission keeps the stored policy. Changing from a non-Runs provider to Runs with an
    absent or {} stored policy requires an explicit network_policy: {"version":"v1","rules":[]} for deny-all or {} for
    unrestricted egress. A nonempty policy requires GKE; with explicit non-GKE placement, send {} for unrestricted
    egress or change placement to GKE. Send {} to clear a policy. Runs responses always include network_policy; {} means
    unrestricted.

     """

    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        
        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        managed_agents_environment_network_policy = cls(
        )


        managed_agents_environment_network_policy.additional_properties = d
        return managed_agents_environment_network_policy

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
