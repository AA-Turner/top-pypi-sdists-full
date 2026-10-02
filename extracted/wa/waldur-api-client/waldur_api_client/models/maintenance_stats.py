from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="MaintenanceStats")


@_attrs_define
class MaintenanceStats:
    """
    Attributes:
        oldest_transaction_age (Union[None, int]): Age of the oldest transaction in transactions
        tables_needing_vacuum (int): Number of tables with high dead tuple ratio
        total_dead_tuples (int): Total estimated dead tuples across all tables
        total_live_tuples (int): Total estimated live tuples across all tables
        dead_tuple_ratio_percent (Union[None, float]): Ratio of dead tuples to total tuples
    """

    oldest_transaction_age: Union[None, int]
    tables_needing_vacuum: int
    total_dead_tuples: int
    total_live_tuples: int
    dead_tuple_ratio_percent: Union[None, float]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        oldest_transaction_age: Union[None, int]
        oldest_transaction_age = self.oldest_transaction_age

        tables_needing_vacuum = self.tables_needing_vacuum

        total_dead_tuples = self.total_dead_tuples

        total_live_tuples = self.total_live_tuples

        dead_tuple_ratio_percent: Union[None, float]
        dead_tuple_ratio_percent = self.dead_tuple_ratio_percent

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "oldest_transaction_age": oldest_transaction_age,
                "tables_needing_vacuum": tables_needing_vacuum,
                "total_dead_tuples": total_dead_tuples,
                "total_live_tuples": total_live_tuples,
                "dead_tuple_ratio_percent": dead_tuple_ratio_percent,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_oldest_transaction_age(data: object) -> Union[None, int]:
            if data is None:
                return data
            return cast(Union[None, int], data)

        oldest_transaction_age = _parse_oldest_transaction_age(d.pop("oldest_transaction_age"))

        tables_needing_vacuum = d.pop("tables_needing_vacuum")

        total_dead_tuples = d.pop("total_dead_tuples")

        total_live_tuples = d.pop("total_live_tuples")

        def _parse_dead_tuple_ratio_percent(data: object) -> Union[None, float]:
            if data is None:
                return data
            return cast(Union[None, float], data)

        dead_tuple_ratio_percent = _parse_dead_tuple_ratio_percent(d.pop("dead_tuple_ratio_percent"))

        maintenance_stats = cls(
            oldest_transaction_age=oldest_transaction_age,
            tables_needing_vacuum=tables_needing_vacuum,
            total_dead_tuples=total_dead_tuples,
            total_live_tuples=total_live_tuples,
            dead_tuple_ratio_percent=dead_tuple_ratio_percent,
        )

        maintenance_stats.additional_properties = d
        return maintenance_stats

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
