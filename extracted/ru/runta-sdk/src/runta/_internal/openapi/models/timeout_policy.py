from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..models.timeout_policy_mode import TimeoutPolicyMode
from ..types import UNSET, Unset

T = TypeVar("T", bound="TimeoutPolicy")


@_attrs_define
class TimeoutPolicy:
    """
    Attributes:
        mode (TimeoutPolicyMode):
        after_seconds (int | Unset): Required for enabled; forbidden for disabled. Explicitly saving restarts only this
            policy’s clock.
    """

    mode: TimeoutPolicyMode
    after_seconds: int | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        mode = self.mode.value

        after_seconds = self.after_seconds

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "mode": mode,
            }
        )
        if after_seconds is not UNSET:
            field_dict["after_seconds"] = after_seconds

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        mode = TimeoutPolicyMode(d.pop("mode"))

        after_seconds = d.pop("after_seconds", UNSET)

        timeout_policy = cls(
            mode=mode,
            after_seconds=after_seconds,
        )

        return timeout_policy
