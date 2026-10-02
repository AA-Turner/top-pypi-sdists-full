from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="OrderStatsSummary")


@_attrs_define
class OrderStatsSummary:
    """
    Attributes:
        total (int): Total number of orders
        total_cost (Union[None, str]): Total cost of orders
        total_revenue (Union[None, str]): Total revenue from create/update orders
        pending (int): Number of pending orders
        executing (int): Number of executing orders
        done (int): Number of completed orders
        erred (int): Number of erred orders
        canceled (int): Number of canceled orders
        rejected (int): Number of rejected orders
    """

    total: int
    total_cost: Union[None, str]
    total_revenue: Union[None, str]
    pending: int
    executing: int
    done: int
    erred: int
    canceled: int
    rejected: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        total = self.total

        total_cost: Union[None, str]
        total_cost = self.total_cost

        total_revenue: Union[None, str]
        total_revenue = self.total_revenue

        pending = self.pending

        executing = self.executing

        done = self.done

        erred = self.erred

        canceled = self.canceled

        rejected = self.rejected

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "total": total,
                "total_cost": total_cost,
                "total_revenue": total_revenue,
                "pending": pending,
                "executing": executing,
                "done": done,
                "erred": erred,
                "canceled": canceled,
                "rejected": rejected,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        total = d.pop("total")

        def _parse_total_cost(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        total_cost = _parse_total_cost(d.pop("total_cost"))

        def _parse_total_revenue(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        total_revenue = _parse_total_revenue(d.pop("total_revenue"))

        pending = d.pop("pending")

        executing = d.pop("executing")

        done = d.pop("done")

        erred = d.pop("erred")

        canceled = d.pop("canceled")

        rejected = d.pop("rejected")

        order_stats_summary = cls(
            total=total,
            total_cost=total_cost,
            total_revenue=total_revenue,
            pending=pending,
            executing=executing,
            done=done,
            erred=erred,
            canceled=canceled,
            rejected=rejected,
        )

        order_stats_summary.additional_properties = d
        return order_stats_summary

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
