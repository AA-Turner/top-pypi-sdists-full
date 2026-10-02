from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.managed_agents_environment_access_expectation_network_policy import ManagedAgentsEnvironmentAccessExpectationNetworkPolicy





T = TypeVar("T", bound="ManagedAgentsEnvironmentAccessExpectation")



@_attrs_define
class ManagedAgentsEnvironmentAccessExpectation:
    """ Request-only precondition for changing an environment's access settings. Supply the network policy and effective
    privileged value from the last environment read; a stale snapshot is rejected.

        Example:
            {'network_policy': {'key': 'example'}, 'privileged': True}

        Attributes:
            network_policy (ManagedAgentsEnvironmentAccessExpectationNetworkPolicy): network_policy from the environment
                read before this PATCH; {} means unrestricted egress.
            privileged (bool): Effective privileged value from the environment read before this PATCH.
     """

    network_policy: ManagedAgentsEnvironmentAccessExpectationNetworkPolicy
    privileged: bool
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.managed_agents_environment_access_expectation_network_policy import ManagedAgentsEnvironmentAccessExpectationNetworkPolicy # noqa: PLC0415
        network_policy = self.network_policy.to_dict()

        privileged = self.privileged


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "network_policy": network_policy,
            "privileged": privileged,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.managed_agents_environment_access_expectation_network_policy import ManagedAgentsEnvironmentAccessExpectationNetworkPolicy # noqa: PLC0415
        d = dict(src_dict)
        network_policy = ManagedAgentsEnvironmentAccessExpectationNetworkPolicy.from_dict(d.pop("network_policy"))




        privileged = d.pop("privileged")

        managed_agents_environment_access_expectation = cls(
            network_policy=network_policy,
            privileged=privileged,
        )


        managed_agents_environment_access_expectation.additional_properties = d
        return managed_agents_environment_access_expectation

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
