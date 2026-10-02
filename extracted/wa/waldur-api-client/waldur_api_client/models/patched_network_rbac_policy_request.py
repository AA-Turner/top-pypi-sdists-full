from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.policy_type_enum import PolicyTypeEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="PatchedNetworkRBACPolicyRequest")


@_attrs_define
class PatchedNetworkRBACPolicyRequest:
    """
    Attributes:
        network (Union[Unset, str]):
        target_tenant (Union[Unset, str]):
        policy_type (Union[Unset, PolicyTypeEnum]):  Default: PolicyTypeEnum.ACCESS_AS_SHARED.
    """

    network: Union[Unset, str] = UNSET
    target_tenant: Union[Unset, str] = UNSET
    policy_type: Union[Unset, PolicyTypeEnum] = PolicyTypeEnum.ACCESS_AS_SHARED
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        network = self.network

        target_tenant = self.target_tenant

        policy_type: Union[Unset, str] = UNSET
        if not isinstance(self.policy_type, Unset):
            policy_type = self.policy_type.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if network is not UNSET:
            field_dict["network"] = network
        if target_tenant is not UNSET:
            field_dict["target_tenant"] = target_tenant
        if policy_type is not UNSET:
            field_dict["policy_type"] = policy_type

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        network = d.pop("network", UNSET)

        target_tenant = d.pop("target_tenant", UNSET)

        _policy_type = d.pop("policy_type", UNSET)
        policy_type: Union[Unset, PolicyTypeEnum]
        if isinstance(_policy_type, Unset):
            policy_type = UNSET
        else:
            policy_type = PolicyTypeEnum(_policy_type)

        patched_network_rbac_policy_request = cls(
            network=network,
            target_tenant=target_tenant,
            policy_type=policy_type,
        )

        patched_network_rbac_policy_request.additional_properties = d
        return patched_network_rbac_policy_request

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
