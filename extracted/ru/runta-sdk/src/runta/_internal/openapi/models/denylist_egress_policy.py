from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define

from ..models.denylist_egress_policy_mode import DenylistEgressPolicyMode

T = TypeVar("T", bound="DenylistEgressPolicy")


@_attrs_define
class DenylistEgressPolicy:
    """Deny matching hosts and allow all other egress destinations.

    Attributes:
        mode (DenylistEgressPolicyMode):
        denied_hosts (list[str]): Host names, wildcard patterns, IP addresses, or CIDR ranges to deny.
    """

    mode: DenylistEgressPolicyMode
    denied_hosts: list[str]

    def to_dict(self) -> dict[str, Any]:
        mode = self.mode.value

        denied_hosts = self.denied_hosts

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "mode": mode,
                "denied_hosts": denied_hosts,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        mode = DenylistEgressPolicyMode(d.pop("mode"))

        denied_hosts = cast(list[str], d.pop("denied_hosts"))

        denylist_egress_policy = cls(
            mode=mode,
            denied_hosts=denied_hosts,
        )

        return denylist_egress_policy
