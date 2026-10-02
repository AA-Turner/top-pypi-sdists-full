from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.policy_enum import PolicyEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="OpenStackNestedServerGroup")


@_attrs_define
class OpenStackNestedServerGroup:
    """
    Attributes:
        url (Union[Unset, str]):
        name (Union[Unset, str]):
        policy (Union[Unset, PolicyEnum]):
        state (Union[Unset, str]):
    """

    url: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    policy: Union[Unset, PolicyEnum] = UNSET
    state: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        url = self.url

        name = self.name

        policy: Union[Unset, str] = UNSET
        if not isinstance(self.policy, Unset):
            policy = self.policy.value

        state = self.state

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if url is not UNSET:
            field_dict["url"] = url
        if name is not UNSET:
            field_dict["name"] = name
        if policy is not UNSET:
            field_dict["policy"] = policy
        if state is not UNSET:
            field_dict["state"] = state

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        url = d.pop("url", UNSET)

        name = d.pop("name", UNSET)

        _policy = d.pop("policy", UNSET)
        policy: Union[Unset, PolicyEnum]
        if isinstance(_policy, Unset):
            policy = UNSET
        else:
            policy = PolicyEnum(_policy)

        state = d.pop("state", UNSET)

        open_stack_nested_server_group = cls(
            url=url,
            name=name,
            policy=policy,
            state=state,
        )

        open_stack_nested_server_group.additional_properties = d
        return open_stack_nested_server_group

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
