from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..models.suspend_only_idle_policy_mode import SuspendOnlyIdlePolicyMode

T = TypeVar("T", bound="SuspendOnlyIdlePolicy")


@_attrs_define
class SuspendOnlyIdlePolicy:
    """Automatically suspend an idle runtime, but require an explicit Start to wake it.

    Attributes:
        mode (SuspendOnlyIdlePolicyMode):
        suspend_after_secs (int): Idle duration before automatic suspension.
    """

    mode: SuspendOnlyIdlePolicyMode
    suspend_after_secs: int

    def to_dict(self) -> dict[str, Any]:
        mode = self.mode.value

        suspend_after_secs = self.suspend_after_secs

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "mode": mode,
                "suspend_after_secs": suspend_after_secs,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        mode = SuspendOnlyIdlePolicyMode(d.pop("mode"))

        suspend_after_secs = d.pop("suspend_after_secs")

        suspend_only_idle_policy = cls(
            mode=mode,
            suspend_after_secs=suspend_after_secs,
        )

        return suspend_only_idle_policy
