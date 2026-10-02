from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="AdminStatsDtoRunsOverTimeItem")



@_attrs_define
class AdminStatsDtoRunsOverTimeItem:
    """ Single day in the run-count time series.

        Attributes:
            date (str): Calendar day for the bucketed run count (ISO-8601 date, UTC).
            runs (float): Number of problem runs that started on this day.
     """

    date: str
    runs: float





    def to_dict(self) -> dict[str, Any]:
        date = self.date

        runs = self.runs


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "date": date,
            "runs": runs,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        date = d.pop("date")

        runs = d.pop("runs")

        admin_stats_dto_runs_over_time_item = cls(
            date=date,
            runs=runs,
        )

        return admin_stats_dto_runs_over_time_item

