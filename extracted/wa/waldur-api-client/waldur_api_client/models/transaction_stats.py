from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="TransactionStats")


@_attrs_define
class TransactionStats:
    """
    Attributes:
        committed (int): Total committed transactions
        rolled_back (int): Total rolled back transactions
        rollback_ratio_percent (float): Percentage of transactions that were rolled back
        deadlocks (int): Total number of deadlocks detected
    """

    committed: int
    rolled_back: int
    rollback_ratio_percent: float
    deadlocks: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        committed = self.committed

        rolled_back = self.rolled_back

        rollback_ratio_percent = self.rollback_ratio_percent

        deadlocks = self.deadlocks

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "committed": committed,
                "rolled_back": rolled_back,
                "rollback_ratio_percent": rollback_ratio_percent,
                "deadlocks": deadlocks,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        committed = d.pop("committed")

        rolled_back = d.pop("rolled_back")

        rollback_ratio_percent = d.pop("rollback_ratio_percent")

        deadlocks = d.pop("deadlocks")

        transaction_stats = cls(
            committed=committed,
            rolled_back=rolled_back,
            rollback_ratio_percent=rollback_ratio_percent,
            deadlocks=deadlocks,
        )

        transaction_stats.additional_properties = d
        return transaction_stats

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
