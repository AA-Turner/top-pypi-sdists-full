from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

from ..models.allowlist_egress_policy_mode import AllowlistEgressPolicyMode

T = TypeVar("T", bound="AllowlistEgressPolicy")


@_attrs_define
class AllowlistEgressPolicy:
    """Allow only matching egress destinations.

    Attributes:
        mode (AllowlistEgressPolicyMode):
        allowed_hosts (list[str]): Host names, wildcard patterns, IP addresses, or CIDR ranges to allow.
    """

    mode: AllowlistEgressPolicyMode
    allowed_hosts: list[str]

    def to_dict(self) -> dict[str, Any]:
        mode = self.mode.value

        allowed_hosts = self.allowed_hosts

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "mode": mode,
                "allowed_hosts": allowed_hosts,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        mode = AllowlistEgressPolicyMode(d.pop("mode"))

        allowed_hosts = cast(list[str], d.pop("allowed_hosts"))

        allowlist_egress_policy = cls(
            mode=mode,
            allowed_hosts=allowed_hosts,
        )

        return allowlist_egress_policy
