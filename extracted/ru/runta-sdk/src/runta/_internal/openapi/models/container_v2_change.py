from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.container_v2_change_action import ContainerV2ChangeAction
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.container_v2_resources import ContainerV2Resources
    from ..models.timeout_policy import TimeoutPolicy


T = TypeVar("T", bound="ContainerV2Change")


@_attrs_define
class ContainerV2Change:
    """
    Attributes:
        action (ContainerV2ChangeAction):
        auto_shutdown_policy (TimeoutPolicy | Unset):
        auto_delete_policy (TimeoutPolicy | Unset):
        name (str | Unset):
        grace_period_seconds (int | Unset):
        resources (ContainerV2Resources | Unset):
    """

    action: ContainerV2ChangeAction
    auto_shutdown_policy: TimeoutPolicy | Unset = UNSET
    auto_delete_policy: TimeoutPolicy | Unset = UNSET
    name: str | Unset = UNSET
    grace_period_seconds: int | Unset = UNSET
    resources: ContainerV2Resources | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        action = self.action.value

        auto_shutdown_policy: dict[str, Any] | Unset = UNSET
        if not isinstance(self.auto_shutdown_policy, Unset):
            auto_shutdown_policy = self.auto_shutdown_policy.to_dict()

        auto_delete_policy: dict[str, Any] | Unset = UNSET
        if not isinstance(self.auto_delete_policy, Unset):
            auto_delete_policy = self.auto_delete_policy.to_dict()

        name = self.name

        grace_period_seconds = self.grace_period_seconds

        resources: dict[str, Any] | Unset = UNSET
        if not isinstance(self.resources, Unset):
            resources = self.resources.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "action": action,
            }
        )
        if auto_shutdown_policy is not UNSET:
            field_dict["auto_shutdown_policy"] = auto_shutdown_policy
        if auto_delete_policy is not UNSET:
            field_dict["auto_delete_policy"] = auto_delete_policy
        if name is not UNSET:
            field_dict["name"] = name
        if grace_period_seconds is not UNSET:
            field_dict["grace_period_seconds"] = grace_period_seconds
        if resources is not UNSET:
            field_dict["resources"] = resources

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.container_v2_resources import ContainerV2Resources
        from ..models.timeout_policy import TimeoutPolicy

        d = dict(src_dict)
        action = ContainerV2ChangeAction(d.pop("action"))

        _auto_shutdown_policy = d.pop("auto_shutdown_policy", UNSET)
        auto_shutdown_policy: TimeoutPolicy | Unset
        if isinstance(_auto_shutdown_policy, Unset):
            auto_shutdown_policy = UNSET
        else:
            auto_shutdown_policy = TimeoutPolicy.from_dict(_auto_shutdown_policy)

        _auto_delete_policy = d.pop("auto_delete_policy", UNSET)
        auto_delete_policy: TimeoutPolicy | Unset
        if isinstance(_auto_delete_policy, Unset):
            auto_delete_policy = UNSET
        else:
            auto_delete_policy = TimeoutPolicy.from_dict(_auto_delete_policy)

        name = d.pop("name", UNSET)

        grace_period_seconds = d.pop("grace_period_seconds", UNSET)

        _resources = d.pop("resources", UNSET)
        resources: ContainerV2Resources | Unset
        if isinstance(_resources, Unset):
            resources = UNSET
        else:
            resources = ContainerV2Resources.from_dict(_resources)

        container_v2_change = cls(
            action=action,
            auto_shutdown_policy=auto_shutdown_policy,
            auto_delete_policy=auto_delete_policy,
            name=name,
            grace_period_seconds=grace_period_seconds,
            resources=resources,
        )

        container_v2_change.additional_properties = d
        return container_v2_change

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
