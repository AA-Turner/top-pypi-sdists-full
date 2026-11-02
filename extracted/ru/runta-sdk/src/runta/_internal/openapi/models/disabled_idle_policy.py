from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..models.disabled_idle_policy_mode import DisabledIdlePolicyMode

T = TypeVar("T", bound="DisabledIdlePolicy")


@_attrs_define
class DisabledIdlePolicy:
    """Disable automatic idle suspension and wakeup.

    Attributes:
        mode (DisabledIdlePolicyMode):
    """

    mode: DisabledIdlePolicyMode

    def to_dict(self) -> dict[str, Any]:
        mode = self.mode.value

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "mode": mode,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        mode = DisabledIdlePolicyMode(d.pop("mode"))

        disabled_idle_policy = cls(
            mode=mode,
        )

        return disabled_idle_policy
