from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.blank_enum import BlankEnum
from ..models.policy_enum import PolicyEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="OpenStackServerGroupRequest")


@_attrs_define
class OpenStackServerGroupRequest:
    """
    Attributes:
        name (str):
        description (Union[Unset, str]):
        policy (Union[BlankEnum, PolicyEnum, Unset]): affinity — all instances are placed on the same hypervisor. anti-
            affinity — all instances are placed on different hypervisors. soft-affinity — instances are placed on the same
            hypervisor if possible, but not enforced. soft-anti-affinity — instances are placed on different hypervisors if
            possible, but not enforced.
    """

    name: str
    description: Union[Unset, str] = UNSET
    policy: Union[BlankEnum, PolicyEnum, Unset] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        description = self.description

        policy: Union[Unset, str]
        if isinstance(self.policy, Unset):
            policy = UNSET
        elif isinstance(self.policy, PolicyEnum):
            policy = self.policy.value
        else:
            policy = self.policy.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if policy is not UNSET:
            field_dict["policy"] = policy

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        description = d.pop("description", UNSET)

        def _parse_policy(data: object) -> Union[BlankEnum, PolicyEnum, Unset]:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                policy_type_0 = PolicyEnum(data)

                return policy_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, str):
                raise TypeError()
            policy_type_1 = BlankEnum(data)

            return policy_type_1

        policy = _parse_policy(d.pop("policy", UNSET))

        open_stack_server_group_request = cls(
            name=name,
            description=description,
            policy=policy,
        )

        open_stack_server_group_request.additional_properties = d
        return open_stack_server_group_request

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
