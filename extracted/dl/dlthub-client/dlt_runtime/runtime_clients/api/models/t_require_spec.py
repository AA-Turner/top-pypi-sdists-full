from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="TRequireSpec")


@_attrs_define
class TRequireSpec:
    """
    Attributes:
        dependency_groups (list[str] | Unset):
        machine (str | Unset):
        profile (str | Unset):
        provider (str | Unset):
        region (str | Unset):
        static_egress_ips (bool | Unset):
        timezone (str | Unset):
    """

    dependency_groups: list[str] | Unset = UNSET
    machine: str | Unset = UNSET
    profile: str | Unset = UNSET
    provider: str | Unset = UNSET
    region: str | Unset = UNSET
    static_egress_ips: bool | Unset = UNSET
    timezone: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        dependency_groups: list[str] | Unset = UNSET
        if not isinstance(self.dependency_groups, Unset):
            dependency_groups = self.dependency_groups

        machine = self.machine

        profile = self.profile

        provider = self.provider

        region = self.region

        static_egress_ips = self.static_egress_ips

        timezone = self.timezone

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if dependency_groups is not UNSET:
            field_dict["dependency_groups"] = dependency_groups
        if machine is not UNSET:
            field_dict["machine"] = machine
        if profile is not UNSET:
            field_dict["profile"] = profile
        if provider is not UNSET:
            field_dict["provider"] = provider
        if region is not UNSET:
            field_dict["region"] = region
        if static_egress_ips is not UNSET:
            field_dict["static_egress_ips"] = static_egress_ips
        if timezone is not UNSET:
            field_dict["timezone"] = timezone

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        dependency_groups = cast(list[str], d.pop("dependency_groups", UNSET))

        machine = d.pop("machine", UNSET)

        profile = d.pop("profile", UNSET)

        provider = d.pop("provider", UNSET)

        region = d.pop("region", UNSET)

        static_egress_ips = d.pop("static_egress_ips", UNSET)

        timezone = d.pop("timezone", UNSET)

        t_require_spec = cls(
            dependency_groups=dependency_groups,
            machine=machine,
            profile=profile,
            provider=provider,
            region=region,
            static_egress_ips=static_egress_ips,
            timezone=timezone,
        )

        t_require_spec.additional_properties = d
        return t_require_spec

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
