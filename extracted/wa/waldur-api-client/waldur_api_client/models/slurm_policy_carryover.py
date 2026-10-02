from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="SlurmPolicyCarryover")


@_attrs_define
class SlurmPolicyCarryover:
    """
    Attributes:
        previous_usage (float):
        carryover_factor (int):
        base_allocation (float):
        unused (float):
        carryover_cap (float):
        carryover (float):
        total_allocation (float):
    """

    previous_usage: float
    carryover_factor: int
    base_allocation: float
    unused: float
    carryover_cap: float
    carryover: float
    total_allocation: float
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        previous_usage = self.previous_usage

        carryover_factor = self.carryover_factor

        base_allocation = self.base_allocation

        unused = self.unused

        carryover_cap = self.carryover_cap

        carryover = self.carryover

        total_allocation = self.total_allocation

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "previous_usage": previous_usage,
                "carryover_factor": carryover_factor,
                "base_allocation": base_allocation,
                "unused": unused,
                "carryover_cap": carryover_cap,
                "carryover": carryover,
                "total_allocation": total_allocation,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        previous_usage = d.pop("previous_usage")

        carryover_factor = d.pop("carryover_factor")

        base_allocation = d.pop("base_allocation")

        unused = d.pop("unused")

        carryover_cap = d.pop("carryover_cap")

        carryover = d.pop("carryover")

        total_allocation = d.pop("total_allocation")

        slurm_policy_carryover = cls(
            previous_usage=previous_usage,
            carryover_factor=carryover_factor,
            base_allocation=base_allocation,
            unused=unused,
            carryover_cap=carryover_cap,
            carryover=carryover,
            total_allocation=total_allocation,
        )

        slurm_policy_carryover.additional_properties = d
        return slurm_policy_carryover

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
