from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

T = TypeVar("T", bound="DailyUsage")


@_attrs_define
class DailyUsage:
    """
    Attributes:
        date (datetime.date):
        vcpu_cost_minor (int):
        memory_cost_minor (int):
        disk_cost_minor (int):
        total_cost_minor (int):
    """

    date: datetime.date
    vcpu_cost_minor: int
    memory_cost_minor: int
    disk_cost_minor: int
    total_cost_minor: int

    def to_dict(self) -> dict[str, Any]:
        date = self.date.isoformat()

        vcpu_cost_minor = self.vcpu_cost_minor

        memory_cost_minor = self.memory_cost_minor

        disk_cost_minor = self.disk_cost_minor

        total_cost_minor = self.total_cost_minor

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "date": date,
                "vcpu_cost_minor": vcpu_cost_minor,
                "memory_cost_minor": memory_cost_minor,
                "disk_cost_minor": disk_cost_minor,
                "total_cost_minor": total_cost_minor,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        date = datetime.date.fromisoformat(d.pop("date"))

        vcpu_cost_minor = d.pop("vcpu_cost_minor")

        memory_cost_minor = d.pop("memory_cost_minor")

        disk_cost_minor = d.pop("disk_cost_minor")

        total_cost_minor = d.pop("total_cost_minor")

        daily_usage = cls(
            date=date,
            vcpu_cost_minor=vcpu_cost_minor,
            memory_cost_minor=memory_cost_minor,
            disk_cost_minor=disk_cost_minor,
            total_cost_minor=total_cost_minor,
        )

        return daily_usage
