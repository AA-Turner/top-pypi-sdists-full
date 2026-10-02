from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="CostStatsDtoCostByOrganizationItem")



@_attrs_define
class CostStatsDtoCostByOrganizationItem:
    """ Cost roll-up for a single organization.

        Attributes:
            id (str): Stable identifier of the bucket: the organization UUID, or the platform sentinel for platform-wide
                spend not attributable to any organization (only present on unscoped responses).
            name (str): Display name of the organization (or platform bucket).
            total_cost (float): Total cost attributed to the organization in USD.
            runs (float): Number of cost records (billed rows) attributed to the organization.
     """

    id: str
    name: str
    total_cost: float
    runs: float





    def to_dict(self) -> dict[str, Any]:
        id = self.id

        name = self.name

        total_cost = self.total_cost

        runs = self.runs


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "id": id,
            "name": name,
            "totalCost": total_cost,
            "runs": runs,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        name = d.pop("name")

        total_cost = d.pop("totalCost")

        runs = d.pop("runs")

        cost_stats_dto_cost_by_organization_item = cls(
            id=id,
            name=name,
            total_cost=total_cost,
            runs=runs,
        )

        return cost_stats_dto_cost_by_organization_item

