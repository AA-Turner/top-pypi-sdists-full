from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.container_v2_spec import ContainerV2Spec
    from ..models.timeout_policy import TimeoutPolicy


T = TypeVar("T", bound="ContainerV2Create")


@_attrs_define
class ContainerV2Create:
    """
    Attributes:
        spec (ContainerV2Spec):
        auto_shutdown_policy (TimeoutPolicy | Unset):
        auto_delete_policy (TimeoutPolicy | Unset):
        name (str | Unset):
        architecture (str | Unset): Optional placement constraint. Omit to use the selected Worker architecture.
    """

    spec: ContainerV2Spec
    auto_shutdown_policy: TimeoutPolicy | Unset = UNSET
    auto_delete_policy: TimeoutPolicy | Unset = UNSET
    name: str | Unset = UNSET
    architecture: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        spec = self.spec.to_dict()

        auto_shutdown_policy: dict[str, Any] | Unset = UNSET
        if not isinstance(self.auto_shutdown_policy, Unset):
            auto_shutdown_policy = self.auto_shutdown_policy.to_dict()

        auto_delete_policy: dict[str, Any] | Unset = UNSET
        if not isinstance(self.auto_delete_policy, Unset):
            auto_delete_policy = self.auto_delete_policy.to_dict()

        name = self.name

        architecture = self.architecture

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "spec": spec,
            }
        )
        if auto_shutdown_policy is not UNSET:
            field_dict["auto_shutdown_policy"] = auto_shutdown_policy
        if auto_delete_policy is not UNSET:
            field_dict["auto_delete_policy"] = auto_delete_policy
        if name is not UNSET:
            field_dict["name"] = name
        if architecture is not UNSET:
            field_dict["architecture"] = architecture

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.container_v2_spec import ContainerV2Spec
        from ..models.timeout_policy import TimeoutPolicy

        d = dict(src_dict)
        spec = ContainerV2Spec.from_dict(d.pop("spec"))

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

        architecture = d.pop("architecture", UNSET)

        container_v2_create = cls(
            spec=spec,
            auto_shutdown_policy=auto_shutdown_policy,
            auto_delete_policy=auto_delete_policy,
            name=name,
            architecture=architecture,
        )

        container_v2_create.additional_properties = d
        return container_v2_create

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
