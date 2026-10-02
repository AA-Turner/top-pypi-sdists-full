from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="SlurmPeriodicUsagePolicyTresBillingWeights")


@_attrs_define
class SlurmPeriodicUsagePolicyTresBillingWeights:
    """TRES billing weights (e.g., {"CPU": 0.015625, "Mem": 0.001953125, "GRES/gpu": 0.25})"""

    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        slurm_periodic_usage_policy_tres_billing_weights = cls()

        slurm_periodic_usage_policy_tres_billing_weights.additional_properties = d
        return slurm_periodic_usage_policy_tres_billing_weights

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
