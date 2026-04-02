from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="SlurmPolicyThresholds")


@_attrs_define
class SlurmPolicyThresholds:
    """
    Attributes:
        allocation (float):
        grace_ratio (float):
        notification_ratio (float):
        notification_threshold (float):
        slowdown_threshold (float):
        blocked_threshold (float):
    """

    allocation: float
    grace_ratio: float
    notification_ratio: float
    notification_threshold: float
    slowdown_threshold: float
    blocked_threshold: float
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        allocation = self.allocation

        grace_ratio = self.grace_ratio

        notification_ratio = self.notification_ratio

        notification_threshold = self.notification_threshold

        slowdown_threshold = self.slowdown_threshold

        blocked_threshold = self.blocked_threshold

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "allocation": allocation,
                "grace_ratio": grace_ratio,
                "notification_ratio": notification_ratio,
                "notification_threshold": notification_threshold,
                "slowdown_threshold": slowdown_threshold,
                "blocked_threshold": blocked_threshold,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        allocation = d.pop("allocation")

        grace_ratio = d.pop("grace_ratio")

        notification_ratio = d.pop("notification_ratio")

        notification_threshold = d.pop("notification_threshold")

        slowdown_threshold = d.pop("slowdown_threshold")

        blocked_threshold = d.pop("blocked_threshold")

        slurm_policy_thresholds = cls(
            allocation=allocation,
            grace_ratio=grace_ratio,
            notification_ratio=notification_ratio,
            notification_threshold=notification_threshold,
            slowdown_threshold=slowdown_threshold,
            blocked_threshold=blocked_threshold,
        )

        slurm_policy_thresholds.additional_properties = d
        return slurm_policy_thresholds

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
