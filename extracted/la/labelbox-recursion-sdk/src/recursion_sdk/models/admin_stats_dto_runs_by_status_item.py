from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="AdminStatsDtoRunsByStatusItem")



@_attrs_define
class AdminStatsDtoRunsByStatusItem:
    """ Run-count bucket for a single status.

        Attributes:
            status (str): Terminal status label for the bucket (e.g. completed, failed).
            runs (float): Number of runs that ended in this status.
     """

    status: str
    runs: float





    def to_dict(self) -> dict[str, Any]:
        status = self.status

        runs = self.runs


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "status": status,
            "runs": runs,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        status = d.pop("status")

        runs = d.pop("runs")

        admin_stats_dto_runs_by_status_item = cls(
            status=status,
            runs=runs,
        )

        return admin_stats_dto_runs_by_status_item

