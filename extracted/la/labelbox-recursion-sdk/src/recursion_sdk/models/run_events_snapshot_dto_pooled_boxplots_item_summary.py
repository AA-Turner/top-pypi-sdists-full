from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast






T = TypeVar("T", bound="RunEventsSnapshotDtoPooledBoxplotsItemSummary")



@_attrs_define
class RunEventsSnapshotDtoPooledBoxplotsItemSummary:
    """ Box-plot five-number summary (min/q1/median/q3/max) plus Tukey-fence outliers.

        Attributes:
            min_ (float): Smallest observed value in the sample.
            q1 (float): First quartile (25th percentile), type-7 interpolation.
            median (float): Median (50th percentile), type-7 interpolation.
            q3 (float): Third quartile (75th percentile), type-7 interpolation.
            max_ (float): Largest observed value in the sample.
            outliers (list[float]): Values outside [q1 - 1.5*IQR, q3 + 1.5*IQR] (Tukey fences).
     """

    min_: float
    q1: float
    median: float
    q3: float
    max_: float
    outliers: list[float]





    def to_dict(self) -> dict[str, Any]:
        min_ = self.min_

        q1 = self.q1

        median = self.median

        q3 = self.q3

        max_ = self.max_

        outliers = self.outliers




        field_dict: dict[str, Any] = {}

        field_dict.update({
            "min": min_,
            "q1": q1,
            "median": median,
            "q3": q3,
            "max": max_,
            "outliers": outliers,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        min_ = d.pop("min")

        q1 = d.pop("q1")

        median = d.pop("median")

        q3 = d.pop("q3")

        max_ = d.pop("max")

        outliers = cast(list[float], d.pop("outliers"))


        run_events_snapshot_dto_pooled_boxplots_item_summary = cls(
            min_=min_,
            q1=q1,
            median=median,
            q3=q3,
            max_=max_,
            outliers=outliers,
        )

        return run_events_snapshot_dto_pooled_boxplots_item_summary

